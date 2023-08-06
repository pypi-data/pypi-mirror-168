import json
from google.oauth2 import service_account
import google.cloud.firestore as firestore
from google.cloud import bigquery
from txp.common.utils import firestore_utils
import datetime
from txp.common.utils import reports_utils, bigquery_utils

credentials_path = "../../common/credentials/pub_sub_to_bigquery_credentials.json"
with open(credentials_path, 'r') as file:
    credentials_str = file.read().replace('\n', '')

json_dict_service_account = json.loads(credentials_str, strict=False)
credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
bigquery_db = bigquery.Client(credentials=credentials, project=credentials.project_id)

w = reports_utils.get_available_reports(firestore_db, bigquery_db, "tranxpert-mvp.reports_test.sections",
                                      "labshowroom-001",
                                      datetime.datetime.strptime("2022-08-15 18:00:00.0+0000",
                                                                 '%Y-%m-%d %H:%M:%S.%f%z'))

print(w)



#bigquery_utils.get_last_task_prediction_for_asset("labshowroom-001", "ml_events_and_states.states", "Showroom_Fridge", 10, bigquery_db)


#
# transitions_path = "./transitions_states.json"
# with open(transitions_path, 'r') as file:
#     transitions = file.read().replace('\n', '')
# transitions = json.loads(transitions, strict=False)
#
#
# bigquery_db.insert_rows_json("tranxpert-mvp.reports_test.sections", [transitions])
#
