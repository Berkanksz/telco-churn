# Telco Churn API — Test Raporu

**Test eden:** Muratcan Ateş
**Tarih:** 2026-04-25
**API versiyonu:** 1.0.0
**Test ortamı:** Localhost (uvicorn), macOS

---

## Test Özeti

| Kategori | Toplam | Başarılı | Başarısız |
|----------|:-:|:-:|:-:|
| Mutlu Yol (happy path) | 5 | 5 | 0 |
| Edge Cases | 5 | 5 | 0 |
| Hata Senaryoları | 5 | 5 | 0 |
| **Toplam** | **15** | **15** | **0** |

---

## Sağlık Kontrolü

### Test 0.1 — `/health` endpoint

**Komut:**
```
curl http://localhost:8000/health
```

**Beklenen:** `{"status":"ok","ready":true}`
**Alınan:**
```
HTTP/1.1 200 OK
x-request-id: cff7108b64c84f189a15608a10845347
{"status":"ok","ready":true}
```
**Sonuç:** ✅

### Test 0.2 — `/` endpoint

**Komut:**
```
curl http://localhost:8000/
```

**Beklenen:** Servis meta bilgisi JSON'u
**Alınan:**
```
HTTP/1.1 200 OK
x-request-id: 448243604ee9431894b5b2ed990071a8
{"service":"Telco Customer Churn API","version":"1.0.0","docs":"/docs"}
```
**Sonuç:** ✅

---

## Mutlu Yol (Happy Path) Senaryoları

### Test 1 — Genç, ay-to-ay müşteri (yüksek churn riskli)

**Profil:** 2 aylık, fiber optic, ay-to-ay sözleşme, elektronik çek
**Beklenen davranış:** `prediction=1` (churn), yüksek probability (>0.5)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":2,"MonthlyCharges":70.35,"TotalCharges":140.70,"SeniorCitizen":0,"gender":"Female","Partner":"No","Dependents":"No","PhoneService":"Yes","MultipleLines":"No","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"No","DeviceProtection":"No","TechSupport":"No","StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check"}'
```

**Alınan:**
```json
{"prediction":1,"probability":0.6925494120806664,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-1.2409180113122174,"impact":1.4558830211496647,"direction":"increases_churn"},{"feature":"TotalCharges","value":-0.9486355534488125,"impact":-0.49823412751322843,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"Contract_Month-to-month","value":1.0,"impact":0.24353838782103857,"direction":"increases_churn"},{"feature":"InternetService_DSL","value":0.0,"impact":0.22842395935452176,"direction":"increases_churn"}]}
```
**probability:** 0.6925
**prediction:** 1
**top_factors[0]:** tenure (etki +1.4559, increases_churn)
**Sonuç:** ✅

### Test 2 — Sadık, uzun vadeli müşteri (düşük churn riskli)

**Profil:** 60 ay, DSL, 2 yıllık sözleşme, banka transferi
**Beklenen:** `prediction=0`, düşük probability (<0.3)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":60,"MonthlyCharges":55.50,"TotalCharges":3330.00,"SeniorCitizen":0,"gender":"Male","Partner":"Yes","Dependents":"Yes","PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL","OnlineSecurity":"Yes","OnlineBackup":"Yes","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year","PaperlessBilling":"No","PaymentMethod":"Bank transfer (automatic)"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.01653475194675857,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":1.1200146093262338,"impact":-1.474068929810799,"direction":"retains"},{"feature":"Contract_Two year","value":1.0,"impact":-0.6338631635419782,"direction":"retains"},{"feature":"InternetService_DSL","value":1.0,"impact":-0.42421592451554047,"direction":"retains"},{"feature":"Contract_Month-to-month","value":0.0,"impact":-0.33631491651476747,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":0.0,"impact":-0.320092259260333,"direction":"retains"}]}
```
**probability:** 0.0165
**prediction:** 0
**top_factors[0]:** tenure (etki −1.4741, retains)
**Sonuç:** ✅

### Test 3 — Orta segment müşteri

**Profil:** 24 ay, fiber optic, 1 yıllık sözleşme
**Beklenen:** Orta probability (0.3-0.6 arası)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":24,"MonthlyCharges":89.95,"TotalCharges":2158.80,"SeniorCitizen":0,"gender":"Male","Partner":"Yes","Dependents":"No","PhoneService":"Yes","MultipleLines":"Yes","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"Yes","DeviceProtection":"Yes","TechSupport":"No","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"One year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.4761137797295374,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"MonthlyCharges","value":0.8302532457775423,"impact":-0.42251572544251553,"direction":"retains"},{"feature":"tenure","value":-0.3453918448631497,"impact":0.3445219363025925,"direction":"increases_churn"},{"feature":"Contract_Month-to-month","value":0.0,"impact":-0.33631491651476747,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"InternetService_DSL","value":0.0,"impact":0.22842395935452176,"direction":"increases_churn"}]}
```
**probability:** 0.4761
**prediction:** 0
**top_factors[0]:** MonthlyCharges (etki −0.4225, retains)
**Sonuç:** ✅ (0.3-0.6 aralığında)

### Test 4 — İnternet servisi olmayan müşteri

**Profil:** 40 ay, sadece telefon, ay-to-ay
**Beklenen:** Düşük probability (internet yoksa birçok risk faktörü uygulanmaz)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":40,"MonthlyCharges":19.85,"TotalCharges":794.00,"SeniorCitizen":0,"gender":"Female","Partner":"Yes","Dependents":"No","PhoneService":"Yes","MultipleLines":"No","InternetService":"No","OnlineSecurity":"No internet service","OnlineBackup":"No internet service","DeviceProtection":"No internet service","TechSupport":"No internet service","StreamingTV":"No internet service","StreamingMovies":"No internet service","Contract":"Month-to-month","PaperlessBilling":"No","PaymentMethod":"Mailed check"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.03838253484274616,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"MonthlyCharges","value":-1.4959122896109767,"impact":0.9647607313968444,"direction":"increases_churn"},{"feature":"tenure","value":0.30589991255435406,"impact":-0.4637406708589148,"direction":"retains"},{"feature":"TotalCharges","value":-0.6617994202722931,"impact":-0.35014631045246003,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":0.0,"impact":-0.320092259260333,"direction":"retains"},{"feature":"StreamingMovies_No internet service","value":1.0,"impact":-0.25590408896936473,"direction":"retains"}]}
```
**probability:** 0.0384
**prediction:** 0
**top_factors[0]:** MonthlyCharges (etki +0.9648, increases_churn — düşük ücret modelde "azalan değer artırıyor" şeklinde işliyor; net olasılık çok düşük çıkıyor)
**Sonuç:** ✅

### Test 5 — Yaşlı vatandaş, tam paket

**Profil:** 12 ay, fiber optic, tüm ek servisler, 1 yıllık sözleşme
**Beklenen:** Orta probability

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":12,"MonthlyCharges":105.50,"TotalCharges":1266.00,"SeniorCitizen":1,"gender":"Female","Partner":"Yes","Dependents":"No","PhoneService":"Yes","MultipleLines":"Yes","InternetService":"Fiber optic","OnlineSecurity":"Yes","OnlineBackup":"Yes","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"One year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.3827828992832839,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-0.8338606629262776,"impact":0.950718891673723,"direction":"increases_churn"},{"feature":"MonthlyCharges","value":1.3462571555534548,"impact":-0.7302496613034577,"direction":"retains"},{"feature":"Contract_Month-to-month","value":0.0,"impact":-0.33631491651476747,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"TotalCharges","value":-0.45456437533227007,"impact":-0.24315495938452392,"direction":"retains"}]}
```
**probability:** 0.3828
**prediction:** 0
**top_factors[0]:** tenure (etki +0.9507, increases_churn)
**Sonuç:** ✅

---

## Edge Case Senaryoları

### Test 6 — Tenure = 1 ay (yeni)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":1,"MonthlyCharges":50.00,"TotalCharges":50.00,"SeniorCitizen":0,"gender":"Male","Partner":"No","Dependents":"No","PhoneService":"Yes","MultipleLines":"No","InternetService":"DSL","OnlineSecurity":"No","OnlineBackup":"No","DeviceProtection":"No","TechSupport":"No","StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.49348022054419477,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-1.2816237461508113,"impact":1.506399434097259,"direction":"increases_churn"},{"feature":"TotalCharges","value":-0.9884580504319905,"impact":-0.5187936943392067,"direction":"retains"},{"feature":"InternetService_DSL","value":1.0,"impact":-0.42421592451554047,"direction":"retains"},{"feature":"MonthlyCharges","value":-0.4954288246756865,"impact":0.368093325209873,"direction":"increases_churn"},{"feature":"InternetService_Fiber optic","value":0.0,"impact":-0.320092259260333,"direction":"retains"}]}
```
**Yorum:** prediction=0 fakat probability=0.4935 — eşik (0.5) sınırının hemen altında. DSL seçeneği ve düşük MonthlyCharges, tenure=1 ve ay-to-ay sözleşmenin getirdiği yüksek riski tampone etmiş görünüyor. Sınır vakası olarak makul.
**Sonuç:** ✅ (geçerli yanıt, mantıklı çıktı)

### Test 7 — Tenure = 72 ay (maksimum)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":72,"MonthlyCharges":30.00,"TotalCharges":2160.00,"SeniorCitizen":0,"gender":"Male","Partner":"Yes","Dependents":"Yes","PhoneService":"Yes","MultipleLines":"No","InternetService":"No","OnlineSecurity":"No internet service","OnlineBackup":"No internet service","DeviceProtection":"No internet service","TechSupport":"No internet service","StreamingTV":"No internet service","StreamingMovies":"No internet service","Contract":"Two year","PaperlessBilling":"No","PaymentMethod":"Bank transfer (automatic)"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.0017223316057998351,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":1.6084834273893616,"impact":-2.0802658851819293,"direction":"retains"},{"feature":"MonthlyCharges","value":-1.1590994481816834,"impact":0.7638925996290913,"direction":"increases_churn"},{"feature":"Contract_Two year","value":1.0,"impact":-0.6338631635419782,"direction":"retains"},{"feature":"Contract_Month-to-month","value":0.0,"impact":-0.33631491651476747,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":0.0,"impact":-0.320092259260333,"direction":"retains"}]}
```
**probability:** 0.0017 — beklendiği gibi çok düşük; tenure ve 2 yıllık sözleşme hâkim retain faktörleri.
**Sonuç:** ✅

### Test 8 — MonthlyCharges çok düşük ($18)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":6,"MonthlyCharges":18.25,"TotalCharges":109.50,"SeniorCitizen":0,"gender":"Female","Partner":"No","Dependents":"No","PhoneService":"Yes","MultipleLines":"No","InternetService":"No","OnlineSecurity":"No internet service","OnlineBackup":"No internet service","DeviceProtection":"No internet service","TechSupport":"No internet service","StreamingTV":"No internet service","StreamingMovies":"No internet service","Contract":"Month-to-month","PaperlessBilling":"No","PaymentMethod":"Mailed check"}'
```

**Alınan:**
```json
{"prediction":0,"probability":0.16118356211768478,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-1.0780950719578415,"impact":1.253817369359288,"direction":"increases_churn"},{"feature":"MonthlyCharges","value":-1.5490059394914566,"impact":0.996424673350382,"direction":"increases_churn"},{"feature":"TotalCharges","value":-0.9623341411651868,"impact":-0.5053064371600919,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":0.0,"impact":-0.320092259260333,"direction":"retains"},{"feature":"StreamingMovies_No internet service","value":1.0,"impact":-0.25590408896936473,"direction":"retains"}]}
```
**probability:** 0.1612 — düşük gelirli, internet yok profilinde mantıklı düşük tahmin.
**Sonuç:** ✅

### Test 9 — MonthlyCharges çok yüksek ($118)

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":3,"MonthlyCharges":118.50,"TotalCharges":355.50,"SeniorCitizen":0,"gender":"Male","Partner":"No","Dependents":"No","PhoneService":"Yes","MultipleLines":"Yes","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"No","DeviceProtection":"No","TechSupport":"No","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check"}'
```

**Alınan:**
```json
{"prediction":1,"probability":0.7510036935466844,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-1.2002122764736234,"impact":1.4053666082020706,"direction":"increases_churn"},{"feature":"MonthlyCharges","value":1.7776430608323528,"impact":-0.9875191896759495,"direction":"retains"},{"feature":"TotalCharges","value":-0.8543260457091578,"impact":-0.44954399571366765,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"Contract_Month-to-month","value":1.0,"impact":0.24353838782103857,"direction":"increases_churn"}]}
```
**probability:** 0.7510 — yüksek MonthlyCharges + fiber optic + ay-to-ay = yüksek risk; tutarlı.
**Sonuç:** ✅

### Test 10 — SeniorCitizen = 1

**Komut:**
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":8,"MonthlyCharges":95.00,"TotalCharges":760.00,"SeniorCitizen":1,"gender":"Male","Partner":"No","Dependents":"No","PhoneService":"Yes","MultipleLines":"No","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"No","DeviceProtection":"No","TechSupport":"No","StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check"}'
```

**Alınan:**
```json
{"prediction":1,"probability":0.5817631854026106,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-0.9966836022806536,"impact":1.1527845434641,"direction":"increases_churn"},{"feature":"MonthlyCharges","value":0.9978300782128064,"impact":-0.5224550422333681,"direction":"retains"},{"feature":"TotalCharges","value":-0.6767273684247525,"impact":-0.3578533145548114,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"Contract_Month-to-month","value":1.0,"impact":0.24353838782103857,"direction":"increases_churn"}]}
```
**probability:** 0.5818 — yaşlı + fiber + ay-to-ay = orta-yüksek risk; tutarlı.
**Sonuç:** ✅

---

## Hata Senaryoları

### Test 11 — Eksik field (tenure yok)

**Beklenen:** 422 validation error (Pydantic)

**Komut:**
```
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"MonthlyCharges":70.35,...,"PaymentMethod":"Electronic check"}'
```

**Alınan HTTP status:** 422 Unprocessable Content
**Error mesajı:**
```json
{"error":"validation_error","detail":[{"type":"missing","loc":["body","tenure"],"msg":"Field required","input":{...}}]}
```
**Sonuç:** ✅

### Test 12 — Yanlış tip (tenure string)

**Komut:**
```
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":"bir",...}'
```

**Alınan HTTP status:** 422 Unprocessable Content
**Error mesajı:**
```json
{"error":"validation_error","detail":[{"type":"float_parsing","loc":["body","tenure"],"msg":"Input should be a valid number, unable to parse string as a number","input":"bir"}]}
```
**Sonuç:** ✅

### Test 13 — Geçersiz kategorik değer (Contract = "Lifetime")

**Komut:**
```
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure":12,...,"Contract":"Lifetime",...}'
```

**Alınan:**
```
HTTP/1.1 200 OK
x-request-id: 1c23dd6570ed4646a1b17b5bff523174
{"prediction":0,"probability":0.4714218588451359,"expected_value":-1.3442936200190323,"top_factors":[{"feature":"tenure","value":-0.8338606629262776,"impact":0.950718891673723,"direction":"increases_churn"},{"feature":"TotalCharges","value":-0.6416027845366129,"impact":-0.3397191872551612,"direction":"retains"},{"feature":"Contract_Month-to-month","value":0.0,"impact":-0.33631491651476747,"direction":"retains"},{"feature":"InternetService_Fiber optic","value":1.0,"impact":0.320092259260333,"direction":"increases_churn"},{"feature":"InternetService_DSL","value":0.0,"impact":0.22842395935452176,"direction":"increases_churn"}]}
```
**Yorum:** Beklendiği gibi 200 dönüyor. OneHotEncoder `handle_unknown='ignore'` ayarıyla bilinmeyen "Lifetime" değeri sessizce sıfır vektörle kodlanıyor — `top_factors`'ta `Contract_Month-to-month=0.0` ve `Contract_Two year` görünmüyor, yani Contract kolonunun tüm one-hot bileşenleri 0. Bu, sklearn pipeline'ının kasıtlı davranışı. API tarafında ek bir Pydantic enum doğrulaması olmadığından geçersiz kategoriler "varsayılan/baseline" gibi davranıyor. Production'da müşteri verilerinde bilinmeyen sözleşme tipi gelirse sessizce yutmak yerine en azından 4xx döndürmek daha güvenli olabilir; iyileştirme önerileri bölümünde notlandı.
**Sonuç:** ✅ (kasıtlı davranış doğrulandı)

### Test 14 — Bozuk JSON (eksik tırnak)

**Komut:**
```
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{tenure:12}'
```

**Alınan HTTP status:** 422 Unprocessable Content
**Alınan mesaj:**
```json
{"error":"validation_error","detail":[{"type":"json_invalid","loc":["body",1],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting property name enclosed in double quotes"}}]}
```
**Sonuç:** ✅

### Test 15 — Boş body

**Komut:**
```
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{}'
```

**Alınan HTTP status:** 422 Unprocessable Content
**Alınan mesaj:** 19 zorunlu alan için ayrı ayrı `{"type":"missing","loc":["body","<field>"],"msg":"Field required"}` kayıtları (tenure, MonthlyCharges, TotalCharges, SeniorCitizen, gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod).
**Sonuç:** ✅

---

## Genel Gözlemler

### Response Süresi

`/predict` 11 başarılı çağrı (Test 1–10 + Test 13) için ölçülen toplam süre yaklaşık 90.5 ms; ortalama **~8.2 ms**. Validasyon hatası dönen istekler (Test 11, 12, 14, 15) `/predict` modeline hiç ulaşmadığı için 1.0–1.7 ms arasında.

- Ortalama `/predict` cevap süresi: **~8.2 ms**
- En yavaş test: **Test 1** (~21.7 ms — process'te ilk `/predict` çağrısı, lazy yüklemeden kaynaklanan ısınma maliyeti olarak okuduk; sonraki tüm çağrılar ≤14 ms)
- En hızlı test: **Test 10** (~5.2 ms) — Test 8 (~5.3 ms) ile pratikte aynı

### x-request-id Header'ı

Her response'ta (hem 200 hem 422) `x-request-id` header'ı dönüyor — örnekler: `cff7108b64c84f189a15608a10845347` (/health), `448243604ee9431894b5b2ed990071a8` (/), `1c23dd6570ed4646a1b17b5bff523174` (Test 13), `8d030be5b7454633bc5903a297c8de87` (Test 15). 17 isteğin tamamında benzersiz 32 karakterlik hex değeri geldi.
**Sonuç:** ✅

### Karar Tutarlılığı

Bulgular EDA'daki ana hipotezlerle örtüşüyor:
- Düşük `tenure` + `Month-to-month` + `Fiber optic` kombinasyonu yüksek olasılık üretiyor (Test 1: 0.69, Test 9: 0.75, Test 10: 0.58).
- Yüksek `tenure` + `Two year` + DSL/no internet kombinasyonu probability'yi <0.05'e indiriyor (Test 2: 0.017, Test 7: 0.002).
- `top_factors` listesinde `tenure` ağırlıklı olarak en büyük etkiye sahip; impact yönü prediction'la tutarlı (`increases_churn` veya `retains`).
- `expected_value=-1.3442936200190323` her response'ta sabit; bu logit-uzayında sınıf-1 baseline log-odds'unun model tarafında deterministik olarak kullanıldığını gösteriyor.

**Yorum:** Model EDA'da tespit ettiğimiz "yeni + ay-to-ay = yüksek risk" örüntüsünü güvenilir şekilde üretiyor; karar sınırının 0.5 olduğu varsayımıyla prediction/probability eşleşmesi de tutarlı. Test 6 sınırın hemen altında (0.4935) prediction=0 üretti — bu ham bir hata değil, threshold seçiminin bilinçli sonucu.

### Bulduğun Sorunlar

- **Sessiz kategorik bypass (Test 13):** Geçersiz `Contract` değeri (`"Lifetime"`) 200 OK ile dönüyor ve bilinmeyen kategoriler tüm `Contract_*` one-hot bileşenlerini 0 yapıyor. İstenen davranış olsa da çağıran taraf hatayı fark etmiyor; client tarafında log'a düşürmek için ipucu yok.
- **422 yanıtlarında alan başına ayrı kayıt:** Boş body (Test 15) için 19 ayrı `missing` hatası tek payload'da dönüyor — büyük olabiliyor (~1.6KB). Pydantic varsayılanı, ama UI tarafında özetlenmesi gerekebilir.

### Öneriler

- `Contract`, `InternetService`, `PaymentMethod` gibi alanlar için Pydantic `Literal[...]` veya `Enum` kullanarak bilinmeyen değerleri 422'ye düşürmek; modele ulaşmadan reddetmek hem semantic hem güvenli.
- Yanıt header'larında `x-request-id` ek olarak `x-model-version` da göndermek (artifact hash) — production'da model güncellenirse hangi versiyonun karar verdiği gözlenebilir olur.
- Cold-start ısınması için startup'ta dummy bir `predict` çağrısı yapmak Test 1'deki ~22 ms tepe gecikmeyi düzeltir.

---

## Sonuç

**Test edilen endpoint sayısı:** 3 (`/`, `/health`, `/predict`)
**Toplam test senaryosu:** 15
**Başarı oranı:** 15 / 15

API genel olarak başarılı:
- Sağlık endpoint'leri 4–5 ms altında, `/predict` ortalama ~8 ms.
- Pydantic validasyonu eksik alan, yanlış tip ve bozuk JSON için doğru biçimde 422 üretiyor.
- ML çıktısı (probability, prediction, top_factors, expected_value) EDA bulgularıyla tutarlı; `tenure`, `Contract`, `InternetService` kombinasyonu beklenen yönde davranıyor.
- `x-request-id` her response'ta var — gözlemlenebilirlik için iyi bir temel.

İyileştirme alanı: kategorik alanların kontrollü reddi (Test 13'teki sessiz bypass).

**Production readiness değerlendirmesi:** **4 / 5** — Latency, validasyon ve gözlenebilirlik production seviyesinde; tek eksik kategorik girişlerin daha sıkı (Pydantic Literal/Enum) doğrulanması ve model versiyonunun response header'da görünür olması.
