from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Bio.Blast import NCBIWWW, NCBIXML
import uuid
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")

jobs = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def is_valid_fasta(sequence: str) -> bool:
    lines = sequence.strip().split("\n")
    if not lines[0].startswith(">"):
        return False
    sequence_lines = "".join(lines[1:])
    return bool(re.match(r"^[ATCGNatcgn\s]+$", sequence_lines))

def run_blast_job(job_id: str, sequence: str):
    """
    Perform the BLAST query and save the results in the in-memory store.
    """
    try:
        if not is_valid_fasta(sequence):
            jobs[job_id] = {"status": "error", "message": "Invalid FASTA format"}
            return

        result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
        blast_record = NCBIXML.read(result_handle)

        matches = [
            {
                "title": alignment.title,
                "length": alignment.length,
                "e_value": hsp.expect,
                "score": hsp.score,
                "identity": hsp.identities,
            }
            for alignment in blast_record.alignments
            for hsp in alignment.hsps
        ]
        jobs[job_id] = {"status": "completed", "results": matches}
    except Exception as e:
        jobs[job_id] = {"status": "error", "message": str(e)}


@app.post("/blast/")
async def submit_blast(sequence: str = Form(...), background_tasks: BackgroundTasks = None):
    """
    Submit a BLAST query as a background job.
    """
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}

    background_tasks.add_task(run_blast_job, job_id, sequence)

    return {"job_id": job_id}


@app.get("/blast/{job_id}")
async def get_blast_results(job_id: str):
    """
    Check the status of a BLAST job and return the results if completed.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job_status = jobs[job_id]
    return job_status
