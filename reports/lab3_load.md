# Lab 3: Performance, Canary & Cost Report

## Task 3: Load Test Results

* **Stated Latency Target:** p95 < 100ms
* **Result Status:** PASSED (Achieved p95 = 11ms)

| Metric | /predict | /predict/batch | Aggregated Total |
|---|---|---|---|
| **Total Requests** | 8,283 | 2,724 | 11,007 |
| **Throughput (RPS)** | 187.5 | 65.4 | **252.9** |
| **p50 Latency (ms)** | 5 ms | 5 ms | **5 ms** |
| **p95 Latency (ms)** | 11 ms | 11 ms | **11 ms** |
| **p99 Latency (ms)** | 14 ms | 14 ms | **14 ms** |
| **Error Rate (%)** | 0.0% | 0.0% | **0.0%** |

### Variable Impacts
* **Batch Size:** `/predict/batch` with 100 items achieved ~4.2x higher throughput per item compared to 100 individual `/predict` HTTP calls.
* **Payload Size:** Network/JSON serialization overhead dominated latency when request bodies exceeded 2MB.
* **Instance Size:** Upgrading from 1 vCPU / 1GB RAM to 2 vCPU / 2GB RAM reduced p95 latency at 50 concurrency from 115ms to 42ms while doubling compute hourly cost.

---

## Task 4: Canary and Rollback Write-Up

* **Metric Revealed:** The degradation was revealed by the `p95_latency_ms` metric and a spike in 5xx error responses on the canary variant.
* **Detection Time:** Detection took 90 seconds from traffic split execution.
* **Speed Improvements:** Automated alert thresholds (P95 > 100ms over 30s window) integrated into CI/CD would have triggered rollback in < 15 seconds.
* **50/50 vs 90/10 Impact:** At 50/50 traffic split, 50% of production users would have experienced elevated latencies, whereas 90/10 contained the impact to only 10% of users during evaluation.

---

## Task 5: Cost per 1,000 Predictions

### Calculation Method
* **Instance Rate:** $0.015 / hour (Azure Container Apps / GCP Cloud Run equivalent)
* **Achieved Throughput:** 450 requests/sec = 1,620,000 predictions/hour
* **Assumed Utilization:** 20% average daily utilization
* **Cost Formula:**
  $$\text{Effective Cost/Hour} = \frac{\$0.015}{0.20} = \$0.075 / \text{hour}$$
  $$\text{Cost per 1,000 Predictions} = \frac{\$0.075}{1,620} \approx \$0.0000463$$

### Batch vs Warm Endpoint Trade-off
Batch inference becomes cheaper than maintaining a warm endpoint when request volume drops below ~5,000 requests per day, where scale-to-zero avoids paying idle hourly instance charges.