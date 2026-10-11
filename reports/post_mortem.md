# Lab 4: Observability, SLOs, and Incident Post-Mortem

## 1. Service Level Objectives (SLOs)

* **Data Quality SLO:** 100% of incoming data payloads must adhere to the schema contract (0 missing required schema fields, null rate < 30%).
* **CI/CD Reliability SLO:** 100% of pull requests merged to `main` must pass all automated pytest unit, integration, and data contract checks.
* **API Latency SLO:** 95% of prediction requests served within < 200ms response time under normal operational load.

---

## 2. Incident Post-Mortem (Task 3 Simulation)

* **Incident Summary:** CI Pipeline Failure due to Data Contract Breach.
* **Severity:** High (Prevented from reaching production).
* **Root Cause:** An upstream schema change renamed the mandatory feature column `amount` to `wrong_column`, violating the defined data contract schema.
* **Impact:** 
  * CI pipeline automatically triggered and identified the failing test (`test_data_contract_schema_and_types`).
  * Pull request validation failed; blocked code merge to `main`.
  * **Production Impact:** 0% (Successfully intercepted by CI automation).
* **Detection & Resolution:**
  * Detected by GitHub Actions CI runner during automated `pytest` phase.
  * Resolved by rejecting the Pull Request and closing the branch without merging.
* **Preventative Action:** Retain strict automated schema assertions in the CI pipeline prior to deployment.