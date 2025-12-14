# Minimal Viable Guard + Cost-Aware LLM Service (MVG + Cost)

본 프로젝트는 **LLM 서비스 운영 관점**에서  
입·출력 안전 레이어와 요청 단위 비용 로깅을 구현하고,  
캐시 및 단가 시나리오에 따른 비용 분포(p50/p95)와 월간 비용을 분석한다.

---

## 1. Project Overview

### 목표
- 입력/출력 **안전 레이어 2개 이상** 구현
- 요청 단위 **토큰·비용 CSV 로깅**
- **p50/p95 비용·지연**, 월간 비용 시뮬레이션
- 캐시·단가 전략에 따른 **비용 절감 분석**

---

## 2. Safety Layers

### (1) Input Safety: PII Masking
- 전화번호 / 이메일 / 주민번호 정규식 마스킹
- 마스킹된 항목 수(`pii_hits`) 로깅

📄 `src/pii_mask.py`
```python
masked_text, pii_hits = mask_pii(user_text)
