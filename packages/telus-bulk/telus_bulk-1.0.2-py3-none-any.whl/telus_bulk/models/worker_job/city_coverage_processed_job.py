from typing import List
from telus_bulk.models.worker_job.address_processing_job import AddressProcessingJob

class CityCoverageProcessedJob(AddressProcessingJob):
    related_party: List[str] = []
