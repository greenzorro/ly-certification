# ly-certification 瓴羊刷题助手

项目包含两个部分：

## 油猴脚本

[⏬ 油猴脚本](https://greasyfork.org/en/scripts/522657-%E7%93%B4%E7%BE%8A%E5%88%B7%E9%A2%98%E5%8A%A9%E6%89%8B)

- 从 [瓴羊认证](https://cert.lydaas.com/cert-ly-online/certification) 模拟考的考试结果页面导出所有试题，保存为表格文件，以供错题记录和分析。
- 答题页面，空格键切换下一题。

操作演示：[Youtube](https://youtu.be/cj5g2tmWmlg) | [Bilibili](https://www.bilibili.com/video/BV1ng61YNEFw/?share_source=copy_web&vd_source=f798a3fc4cecc541856bed48b800e237)

## 本地脚本

.py文件在本地运行：

- 把油猴脚本导出的考试记录合并整理，整合成PDF错题集，方便复习。
- 根据已有的刷题记录估算整个题库试题数量。
- 积累的题足够多时，可以（近似）生成整个题库。

---

由 [Victor_42](https://victor42.work/) 创造

# For Agent

Two halves: (1) a Tampermonkey script on the Lydaas certification exam site to export questions, (2) a local Python job to merge exports into a wrong-question PDF. Install/verify both, run one end-to-end pass if data exists, then hand studying to the human.

## Prerequisites

- Browser + Tampermonkey for `https://cert.lydaas.com/cert-ly-online/exam/test*`
- Python 3 with `pandas` and `markdown_pdf` (install if missing)
- Human access to the certification site (login / exam session)

## Steps

### A. Browser export

1. Install `browser-script.js` via Tampermonkey (or the GreasyFork link in this README).
2. **One handoff:** human logs into [瓴羊认证](https://cert.lydaas.com/cert-ly-online/certification), opens a practice/exam result page that matches `@match`.
3. Use the script to export the question table (CSV named like `ly_exam_*.csv` into the system Downloads folder) and confirm Space advances questions on the answering UI if that feature is in scope.
4. Stop browser automation once a CSV is on disk.

### B. Local Python

1. From the repo root, ensure deps are installed, then:
   ```bash
   python run.py
   ```
2. The script moves `ly_exam_*.csv` from `~/Downloads` into `records/`, merges/dedupes, estimates bank size when enough exams exist, and builds a PDF wrong-question pack.
3. Verify new files under `records/` and any generated PDF. Then stop.

## Hand off to the human

- Taking exams / studying from the PDF
- Site login and any anti-bot challenges

## Red lines

- Do not bypass exam integrity controls or share answer keys publicly as “automation”
- Do not commit personal exam CSVs or PDFs with private data
- Keep `@match` on the Lydaas exam hosts above
