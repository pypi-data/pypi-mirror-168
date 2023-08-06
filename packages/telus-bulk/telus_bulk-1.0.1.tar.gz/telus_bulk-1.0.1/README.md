# telus-bulk-types-pypi

## Import models using

    from telus_bulk.models

## E.g
    from telus_bulk.models.worker_job import AddressProcessingJob
    job_data: AddressProcessingJob = AddressProcessingJob.parse_raw(message.data)
