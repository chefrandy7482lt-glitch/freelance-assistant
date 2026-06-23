from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from pricing_engine import calculate_price
from tdu_value_engine import compute_task_value
from tdu_domain_registry import get_registered_domains

app = FastAPI()

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------------------------------------------------
# ROOT – FRONTEND
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("static/index.html")


# ---------------------------------------------------------
# CORE FREELANCE JOB PROCESSING
# ---------------------------------------------------------
@app.post("/process_task")
async def process_task(request: Request):
    body = await request.json()
    user_task = body.get("task", "")

    if not user_task:
        return JSONResponse({"error": "No task provided"}, status_code=400)

    # Value engine
    value_score = compute_task_value(user_task)

    # Pricing engine
    price = calculate_price(value_score)

    # Domain registry
    domains = get_registered_domains()

    return {
        "task": user_task,
        "value_score": value_score,
        "price": price,
        "domains": domains,
        "status": "processed"
    }


# ---------------------------------------------------------
# FULL PROJECT PROPOSAL GENERATOR
# ---------------------------------------------------------
@app.post("/generate_proposal")
async def generate_proposal(request: Request):
    body = await request.json()
    task = body.get("task", "")

    if not task:
        return JSONResponse({"error": "No task provided"}, status_code=400)

    proposal = f"""
PROJECT PROPOSAL

Task Summary:
{task}

Objectives:
- Understand the client's needs
- Define deliverables clearly
- Establish timeline and milestones
- Provide transparent pricing

Deliverables:
1. Initial draft
2. Revisions based on feedback
3. Final polished version
4. Optional extended support

Timeline:
- Day 1: Intake + planning
- Day 2–3: Draft creation
- Day 4: Review + revisions
- Day 5: Final delivery

Pricing:
Pricing is based on task complexity and value score.

Status: Proposal generated successfully.
"""

    return {"proposal": proposal.strip()}


# ---------------------------------------------------------
# PC JANITOR – STANDALONE JOBS (SIMULATED, INSTANT)
# ---------------------------------------------------------
@app.post("/pc/clean_temp")
async def pc_clean_temp(request: Request):
    body = await request.json()
    job_name = body.get("job", "PC Temp Cleanup")

    report = {
        "job": job_name,
        "actions": [
            "Scanned system for temporary files",
            "Identified 42 temporary files",
            "Simulated cleanup of temporary files"
        ],
        "status": "completed",
        "note": "All work is simulated and instantaneous within the freelance system."
    }
    return report


@app.post("/pc/scan_system")
async def pc_scan_system(request: Request):
    body = await request.json()
    job_name = body.get("job", "PC System Scan")

    report = {
        "job": job_name,
        "checks": [
            "Disk usage analysis",
            "Startup program review",
            "Log file inspection"
        ],
        "status": "completed",
        "risk_level": "low",
        "note": "Scan is virtual and does not access the user's actual computer."
    }
    return report


@app.post("/pc/cleanup_report")
async def pc_cleanup_report(request: Request):
    body = await request.json()
    job_name = body.get("job", "PC Cleanup Report")

    report = {
        "job": job_name,
        "summary": "PC cleanup simulation completed. No real files were modified.",
        "recommendations": [
            "Remove unused applications",
            "Clear browser cache regularly",
            "Review startup programs monthly"
        ],
        "status": "completed"
    }
    return report


# ---------------------------------------------------------
# EMAIL JANITOR – STANDALONE JOBS (SIMULATED)
# ---------------------------------------------------------
@app.post("/email/clean_inbox")
async def email_clean_inbox(request: Request):
    body = await request.json()
    job_name = body.get("job", "Email Inbox Cleanup")

    result = {
        "job": job_name,
        "simulated_actions": [
            "Identified newsletters and promotions",
            "Grouped low-priority messages",
            "Suggested archive for old threads"
        ],
        "status": "completed",
        "note": "No real email account is accessed; this is a virtual cleanup plan."
    }
    return result


@app.post("/email/summarize_unread")
async def email_summarize_unread(request: Request):
    body = await request.json()
    job_name = body.get("job", "Unread Email Summary")

    summary = {
        "job": job_name,
        "unread_count_estimate": 27,
        "categories": {
            "important": 5,
            "newsletters": 12,
            "notifications": 10
        },
        "status": "completed",
        "note": "Summary is simulated based on typical inbox patterns."
    }
    return summary


@app.post("/email/organize_labels")
async def email_organize_labels(request: Request):
    body = await request.json()
    job_name = body.get("job", "Email Label Organization")

    plan = {
        "job": job_name,
        "suggested_labels": [
            "Clients",
            "Finance",
            "Personal",
            "Newsletters",
            "Notifications"
        ],
        "status": "completed",
        "note": "This is an organizational plan; no real labels are changed."
    }
    return plan


# ---------------------------------------------------------
# FILE ASSISTANT – STANDALONE JOBS (SIMULATED)
# ---------------------------------------------------------
@app.post("/file/summarize")
async def file_summarize(request: Request):
    body = await request.json()
    filename = body.get("filename", "unknown_file.txt")
    content = body.get("content", "")

    if not content:
        summary = "No content provided. Unable to generate summary."
    else:
        summary = f"Summary for {filename}: This file appears to contain {len(content.split())} words."

    return {
        "filename": filename,
        "summary": summary,
        "status": "completed",
        "note": "File content is provided by the user; no files are read from their computer."
    }


@app.post("/file/convert_text")
async def file_convert_text(request: Request):
    body = await request.json()
    filename = body.get("filename", "unknown_file.txt")
    content = body.get("content", "")
    target_format = body.get("target_format", "plain_text")

    converted = content  # For now, just echo content as "converted"

    return {
        "filename": filename,
        "target_format": target_format,
        "converted_preview": converted[:200],
        "status": "completed",
        "note": "Conversion is simulated; no real file system operations are performed."
    }


@app.post("/file/metadata")
async def file_metadata(request: Request):
    body = await request.json()
    filename = body.get("filename", "unknown_file.txt")
    content = body.get("content", "")

    metadata = {
        "filename": filename,
        "size_in_chars": len(content),
        "word_count": len(content.split()) if content else 0,
        "status": "completed",
        "note": "Metadata is computed from provided content only."
    }
    return metadata
