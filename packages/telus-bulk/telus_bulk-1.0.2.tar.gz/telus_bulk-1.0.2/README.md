# telus-bulk-types-pypi

## Import models using

    from telus_bulk.models

## E.g
    from telus_bulk.models.worker_job import AddressProcessingJob
    job_data: AddressProcessingJob = AddressProcessingJob.parse_raw(message.data)

# Changelog
1.0.2:
- Added CityCoverageProcessedJob class
- CSQI service supports a PlaceAms as Place