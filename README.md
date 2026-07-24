# ly-certification 瓴羊刷题助手

油猴脚本 + 本地整理：在瓴羊认证里答题导出，再把多次导出合并成 PDF 错题集（题库足够时还可估算规模）。你负责登录答题与复习；本机安装与 `run.py` 整理交给 Agent。

## 油猴脚本

- 在 [瓴羊认证](https://cert.lydaas.com/cert-ly-online/certification) 模拟考**结果页**导出全部试题为表格，方便错题记录与分析。
- 答题页可用**空格键**切下一题。

操作演示：[Youtube](https://youtu.be/cj5g2tmWmlg) | [Bilibili](https://www.bilibili.com/video/BV1ng61YNEFw/?share_source=copy_web&vd_source=f798a3fc4cecc541856bed48b800e237)

## 本地整理

Agent 跑本地脚本后，会把多次导出的考试记录合并成 PDF 错题集，并在记录足够时估算/逼近题库规模——方便复习，不用手搓表格。

---

由 [Victor_42](https://victor42.work/) 创造

---

# For Agent

Two halves: (1) Tampermonkey on the Lydaas exam site to export questions, (2) local CLI `run.py` to merge exports into PDFs. Install both; operate `run.py` whenever new CSVs arrive.

## Prerequisites

- Browser + Tampermonkey for `https://cert.lydaas.com/cert-ly-online/exam/test*`
- Python 3 with `pandas` and `markdown_pdf`
- Access to the certification site (login is human)

## Install / first-time setup

### A. Browser

1. Install `browser-script.js` via Tampermonkey, or https://greasyfork.org/en/scripts/522657-%E7%93%B4%E7%BE%8A%E5%88%B7%E9%A2%98%E5%8A%A9%E6%89%8B
2. Ask once for login and a matching exam/result page.
3. Confirm export works (CSV `ly_exam_*.csv` in Downloads) and Space advances questions if in scope.

### B. Local Python

```bash
pip install pandas markdown_pdf   # if missing
```

## Usage

When new exam CSVs are in Downloads (or already under `records/`):

```bash
python run.py
```

Behavior:

- Moves `ly_exam_*.csv` from `~/Downloads` into `records/`
- Dedupes / merges records
- With ≥2 exams, estimates bank size; if coverage > ~90%, may export an approximate full-bank PDF to Downloads
- Exports an incorrect-question PDF when wrong answers exist
- With only one exam: still builds wrong-question PDF; cannot estimate bank size

Re-run after each new export.

## Hand off to the human

- Taking exams / studying PDFs
- Site login and anti-bot challenges

## Red lines

- Do not bypass exam integrity controls or publish answer keys as “automation”
- Do not commit personal exam CSVs/PDFs
- Keep `@match` on the Lydaas exam hosts above
