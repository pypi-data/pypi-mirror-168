from os import getenv
from pathlib import Path
from fire import Fire
from odt_to_pdf import file_to_string, string_to_file, convert_odt_to_pdf
from celery import Celery

from odt_to_pdf.queue_name import QUEUE_NAME

app = Celery()

def main(input_file: str='', broker_url: str='redis://redis:6379', result_backend: str='redis://redis:6379'):
  if input_file:
    input_path = Path(input_file)
  else:
    input_path = Path(__file__).parent / 'sample.odt'
  data = file_to_string(input_path)
  app.conf.broker_url = broker_url
  app.conf.result_backend = result_backend
  result = convert_odt_to_pdf.apply_async(
    args=(data, ),
    queue=getenv('CELERY_QUEUE_NAME', QUEUE_NAME),
  )

  outcome = result.wait(60)
  as_file = string_to_file(outcome, file_type='pdf')

  print(as_file.name)
  

if __name__ == '__main__':
  Fire(main)