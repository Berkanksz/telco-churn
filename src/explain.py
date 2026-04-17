"""SHAP-based explainability utilities for single churn predictions."""

import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline


def get_top_factors(
    pipeline: Pipeline,
    X_single: pd.DataFrame,
    top_n: int = 5,
) -> list[dict]:
    """Return the top ``top_n`` features driving a single customer's churn prediction.

    Each factor is reported as a dict with three keys:
        - ``feature``: the cleaned feature name (``num__``/``cat__`` prefix stripped).
        - ``impact``:  the absolute SHAP value (magnitude of contribution).
        - ``direction``: ``'increases_churn'`` if the SHAP value is positive,
          ``'decreases_churn'`` otherwise.
    """
    preprocessor = pipeline.named_steps['preprocessor']
    classifier = pipeline.named_steps['classifier']

    X_transformed = preprocessor.transform(X_single)
    feature_names = _clean_feature_names(preprocessor.get_feature_names_out())

    explainer = shap.LinearExplainer(classifier, X_transformed)
    shap_values = explainer(X_transformed).values
    values = _positive_class_values(shap_values)

    abs_values = np.abs(values)
    top_indices = np.argsort(abs_values)[::-1][:top_n]

    return [
        {
            'feature': feature_names[idx],
            'impact': float(abs_values[idx]),
            'direction': 'increases_churn' if values[idx] > 0 else 'decreases_churn',
        }
        for idx in top_indices
    ]


def _clean_feature_names(raw_names) -> list[str]:
    """Strip the ColumnTransformer ``num__`` / ``cat__`` prefixes from feature names."""
    return [name.replace('num__', '').replace('cat__', '') for name in raw_names]


def _positive_class_values(shap_values) -> np.ndarray:
    """Return the 1-D SHAP values for the positive (churn) class of the first sample.

    Handles both legacy SHAP output (list of per-class arrays) and the newer
    3-D array layout ``(n_samples, n_features, n_classes)``.
    """
    if isinstance(shap_values, list):
        return shap_values[1][0]
    values = np.asarray(shap_values)
    if values.ndim == 3:
        return values[0, :, 1]
    return values[0]
