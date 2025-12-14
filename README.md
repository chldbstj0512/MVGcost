# Minimal Viable Guard + Cost-Aware LLM Service (MVG + Cost)

본 프로젝트는 **LLM 서비스 운영 관점**에서  
입·출력 안전 레이어와 요청 단위 비용 로깅을 구현하고,  
캐시 및 단가 시나리오에 따른 비용 분포(p50/p95)와 월간 비용을 분석한다.

> 본 프로젝트는 실제 LLM API 호출 없이,  
> 더미 응답을 활용한 **운영·비용 시뮬레이션**에 초점을 둔다.

---

## 1. Project Overview

### 목표
- 입력/출력 **안전 레이어 2개 이상** 구현
- 요청 단위 **토큰·비용 CSV 로깅**
- **p50/p95 비용·지연** 분석
- 캐시 전략을 가정한 **월간 비용 시뮬레이션**
- 비용 절감 전략에 대한 분석적 제안

---

## 2. Safety Layers

### (1) Input Safety: PII Masking
- 전화번호 / 이메일 / 주민번호 정규식 기반 마스킹
- 마스킹된 항목 수(`pii_hits`)를 로그로 기록
- 개인정보가 모델 입력으로 전달되지 않도록 차단

---

### (2) Output Safety: Moderation
- 휴리스틱 기반 유해 키워드 검사
- 정책 위반 시 응답을 차단하고 정책 문구로 대체
- 차단 여부(`blocked`)를 CSV 로그에 기록

---

## 3. Cost Logging

- 토큰 수는 `tiktoken`으로 계산  
  (미설치 시 문자 수 기반 폴백 사용)
- 요청 단위 비용을 CSV로 로깅
- 캐시 적중 요청은 비용을 **0**으로 처리하여  
  캐시 전략의 비용 절감 효과를 시뮬레이션

---

## 4. Analysis & Scenarios

- **Case 1 (Baseline)**  
  - Cache Hit Rate = 0.0  
  - price_per_1k = 0.002  

- **Case 2 (Cache Applied)**  
  - Cache Hit Rate = 0.4  
  - price_per_1k = 0.002  

각 시나리오에 대해:
- 요청 비용 분포 히스토그램
- p50 / p95 비용 비교
- Top-N 고비용 요청 분석
- 평균 요청 비용 기반 월간 비용 추정

분석 및 시각화는 `analyze.ipynb`에서 수행한다.

---

## 5. Repository Structure

```text
mvg-cost-mini/
├─ README.md
├─ requirements.txt
├─ data/
│  └─ prompts.csv
├─ logs/
│  └─ access_cost_log.csv
├─ src/
│  ├─ pii_mask.py
│  ├─ moderation.py
│  ├─ tokenizer.py
│  ├─ cost.py
│  └─ pipeline.py
├─ run_pipeline.py
└─ analyze.ipynb
```
