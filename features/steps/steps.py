from behave import given, when, then
import requests
import utilities.rw_csv as csv
from utilities.resources import ApiResources
from utilities.log import custom_logger as log

log = log()
log.info("\n\n\n\n***************************************NEW RUN*****************************************************")


@given(u'I set base REST API url and headers correctly')
def setup_baseurl(context):
    try:
        context.baseURL = context.config.userdata.get("base_url", "url")
        context.headers = {"token": context.config.userdata.get("access_token", "token"),
                           "content-type": "application/json"}
        context.ad_account_id = context.config.userdata.get("account_id", "1001")
        log.info(f"Base URL set to : {context.baseURL}")
        log.info(f"Headers set to : {context.headers}")
        log.info(f"account_id set to : {context.ad_account_id}")
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Set csv path to {csv_file_path}')
def set_csv_path(context, csv_file_path='data/PO_API Automation - Sheet1.csv'):
    try:
        context.csv_file_path = csv_file_path
        log.info(f"CSV path set to: {context.csv_file_path}")
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Execute test case {testcase_id}')
def get_testcase_data(context, testcase_id):
    try:
        context.testcase_id = testcase_id
        # Fetching all data from the provided testcase_id from the CSV file
        context.row = csv.read_csv(testcase_id, key="row", csv_file_path=context.csv_file_path)
        try:
            # Check if CSV file returned any error
            if context.row["error"]: raise context.row["error_msg"]
        except Exception as e:
            # If the error is not raised for "error" key not in row (context.row["error"]) log and raise error message
            if "error" not in str(e):
                log.exception(e)
                raise e
        log.info(f'<{context.testcase_id}> - CSV File row data: {context.row}')
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'I set api endpoint to {endpoint}')
def set_endpoint(context, endpoint):
    try:
        # context.endpoint = f"adaccount/{context.account_id}/tactic"
        context.ep = endpoint
        context.endpoint = f"ApiResources.{endpoint}"
        context.endpoint = eval(eval(f'{context.endpoint}'))
        log.info(f"<{context.testcase_id}> - Endpoint set to : {context.endpoint}")
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Set the body of request to {body}')
def set_body(context, body):
    try:
        # Get body code from CSV file row
        context.body = context.row[body.capitalize()] if body.lower() != 'blank' else "{}"
        log.info(f"<{context.testcase_id}> - Body set to: {context.body}")
        # log.debug(f"context.body :type{type(context.body)}, plain {context.body}, str:{str(context.body)}")
        # if context.body == "": raise Exception("There is no data in body")
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Perform post')
def perform_post(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing post")
        context.response = requests.post(context.baseURL + context.endpoint, data=context.body.encode('utf-8'), headers=context.headers)
        log.info(f'<{context.testcase_id}> - POST Response: {context.response.json()}')
        if str(context.ep) == "create_tactic" and context.response.json()["data"]["success"]:
            get_tactic_id(context)
            context.tactic = True
        elif str(context.ep) == "create_step_1":
            context.tactic = False
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Perform get')
def perform_get(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing GET")
        context.response = requests.get(context.baseURL + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - GET Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e

@when(u'Perform put')
def perform_put(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing PUT")
        if context.endpoint == "adaccount/36/tactic":
            context.body= context.body.replace('+f"{context.tactic_id}"+',str(context.tactic_id))
        context.response = requests.put(context.baseURL + context.endpoint, data=context.body.encode('utf-8'),
                                        headers=context.headers)
        log.info(f'<{context.testcase_id}> - PUT Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e

@when(u'Perform delete')
def perform_delete(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing DELETE")
        context.response = requests.delete(context.baseURL + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - DELETE Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e

@then(u'Validate HTTP response code')
def validate_response_code(context):
    try:
        # Get response code from CSV file
        context.response_code = context.row["Expected status code"]
        # csv.read_csv(context.testcase_id, key="Expected status code")
        log.info(f"<{context.testcase_id}> - Actule Response Code: {context.response.status_code}")
        log.info(f"<{context.testcase_id}> - Expected Response Code: {context.response_code}")
        assert str(context.response.status_code) == context.response_code, \
            log.exception(f"<{context.testcase_id}> - Actule Response Code({context.response.status_code})does not "
                          f"matches Expected Response Code({context.response_code})")
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate error {error_from}')
def validate_response_error(context,error_from):
    try:
        # Get err_code from CSV file
        err_code = context.row["Error"] if error_from=="from csv" else error_from.lower()
        context.actual_err_code = context.response.json()["error"]
        # csv.read_csv(context.testcase_id, key="Error")
        log.info(f'<{context.testcase_id}> - Actule Error Code: {context.actual_err_code}')
        log.info(f'<{context.testcase_id}> - Expected Error Code: {err_code}')
        assert str(context.response.json()["error"]).lower() == err_code.lower(), \
            log.exception(
                f'<{context.testcase_id}> - Actule Error Code ({context.response.json()["error"]}'
                f' does not matches Expected Error Code ({err_code})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Extract tactic Id')
def get_tactic_id(context):
    try:
        context.tactic_id = context.response.json()["data"]["tactic_id"]
        print(f'<{context.testcase_id}> - Tactic Id: {context.tactic_id}')
        log.info(f'<{context.testcase_id}> - Tactic Id: {context.tactic_id}')
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate the status')
def validate_status(context):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)
            context.actual_status = context.response.json()["data"]["status"]
            context.expected_status = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_status}')
            assert str(context.actual_status).lower() == context.expected_status.lower(), \
                log.exception(
                    f'<{context.testcase_id}> - Actule Tactic status ({context.actual_status}'
                    f' does not matches Expected Error Code ({context.expected_status})')
        else:
            log.info(f'<{context.testcase_id}> - Validate the status Response: STEP SKIPPED. The tactic was not created\
            , So there is no tactic to Validate the status.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate the date_schedule')
def validate_date_schedule(context):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)
            context.actual_date_schedule = context.response.json()["data"]["tactic_json"]["date_schedule"]
            context.expected_date_schedule = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_date_schedule}')
            assert str(context.actual_date_schedule).lower() == context.expected_date_schedule.lower(), \
                log.exception(
                    f'<{context.testcase_id}> - Actule Tactic status ({context.actual_date_schedule}'
                    f' does not matches Expected Error Code ({context.expected_date_schedule})')
        else:
            log.info(f'<{context.testcase_id}> - Validate the date_schedule Response: STEP SKIPPED. The tactic was not\
             created, So there is no tactic to Validate the date_schedule.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate the {date}')
def validate_date(context, date):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)

            context.actual_date = context.response.json()["data"]["date"]
            context.expected_date = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_date}')
            assert str(context.actual_date).lower() == context.expected_date.lower(), \
                log.exception(
                    f'<{context.testcase_id}> - Actule Tactic status ({context.actual_date}'
                    f' does not matches Expected Error Code ({context.expected_date})')
        else:
            log.info(f'<{context.testcase_id}> - Validate the date_schedule Response: STEP SKIPPED. The tactic was not\
             created, So there is no tactic to Validate the {date}.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Delete the tactic')
def del_tactic(context):
    try:
        if context.tactic:
            context.del_response = requests.delete(
                context.baseURL + f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}",
                headers=context.headers)
            log.info(f'<{context.testcase_id}> - DELETE Response: {context.del_response.json()}')
        else:
            log.info(f'<{context.testcase_id}> - DELETE Response: STEP SKIPPED. The tactic was not created, So there is\
             no tactic to delete.')
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate success')
def validate_success(context):
    try:
        context.actual_status = context.response.json()["data"]["success"]
        # if context.endpoint != f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}" else context.response.json()["data"]["Success"]
        context.expected_status = context.row['Validate']
        log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_status}')
        assert str(context.actual_status).lower() == context.expected_status.lower(), \
            log.exception(
                f'<{context.testcase_id}> - Actule Tactic status ({context.actual_status}'
                f' does not matches Expected Error Code ({context.expected_status})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e
@then(u'Validate Success1')
def validate_success1(context):
    try:
        context.actual_status = context.response.json()["data"]["Success"]
        # if context.endpoint != f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}" else context.response.json()["data"]["Success"]
        context.expected_status = context.row['Validate']
        log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_status}')
        assert str(context.actual_status).lower() == context.expected_status.lower(), \
            log.exception(
                f'<{context.testcase_id}> - Actule Tactic status ({context.actual_status}'
                f' does not matches Expected Error Code ({context.expected_status})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e

@then(u'validate pages')
def validate_pages(context):
    try:
        context.actual_pages = context.response.json()["data"]["pages"]
        log.info(f'<{context.testcase_id}> - Actule number of pages: {context.actual_pages}')
        assert context.actual_pages != 0, \
            log.exception(
                f'<{context.testcase_id}> - Actule pages ({context.response.json()["data"]["pages"]}'
                f' does not matches Expected pages that is greter than 0')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'validate page_size')
def validate_page_size(context):
    try:
        context.actual_page_size = context.response.json()["data"]["page_size"]
        log.info(f'<{context.testcase_id}> - Actule number of pages: {context.actual_page_size}')
        assert context.actual_page_size == 10 and context.actual_page_size != None, \
            log.exception(
                f'<{context.testcase_id}> - Actule pages ({context.response.json()["data"]["page_size"]}'
                f' does not matches Expected page size ({context.actual_page_size})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e

@then(u'validate current_page')
def validate_current_page(context):
    try:
        context.current_page = context.response.json()["data"]["current_page"]
        log.info(f'<{context.testcase_id}> - Actule number of pages: {context.current_page}')
        assert context.current_page == 1, \
            log.exception(
                f'<{context.testcase_id}> - Actule pages ({context.response.json()["data"]["pages"]}'
                f' does not matches Expected count of current page  ({context.current_page})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e

@then(u'validate total count of tactic on overview')
def validate_count(context):
    try:
        context.count = context.response.json()["data"]["count"]
        log.info(f'<{context.testcase_id}> - Actule number of pages: {context.count}')
        assert context.count != 0, \
            log.exception(
                f'<{context.testcase_id}> - Actule pages ({context.response.json()["data"]["count"]}'
                f' does not matches Expected count of current page  ({context.count})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e

@then(u'Validate tactic id from {get_tacticid}')
def validate_tactic_id(context,get_tacticid):
    try:
        #If input is "overview" then get tactic id from overview
        #Else get tactic id from get tactic data method
        context.id = context.response.json()["data"]["results"][0]["id"] if get_tacticid.lower()=="overview" else context.response.json()["data"]["id"]
        log.info(f'<{context.testcase_id}> - Actule number of pages: {context.tactic_id}')
        assert context.tactic_id == context.id, \
            log.exception(
                f'<{context.testcase_id}> - Actule tactic id from overview is  ({context.id}'
                f' does not matches Expected tactic id after tactic creation({context.tactic_id})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e

# @then(u'Validate tactic id from task overview')
# def validate_task_overview(context):
#     try:
#         context.id_overview = context.response.json()["data"][0]["id"]
#         log.info(f'<{context.testcase_id}> - tactic id on overview is: {context.tactic_id}')
#         assert context.tactic_id == context.id_overview, \
#             log.exception(
#                 f'<{context.testcase_id}> - Actule tactic id from overview is  ({context.id_overview}'
#                 f' does not matches Expected tactic id after tactic creation({context.tactic_id})')
#     except AssertionError as e:
#         log.exception(e)
#         raise e
#     except Exception as e:
#         log.exception(str(e))
#         raise e

@then(u'Validate message {message}')
def validate_massage(context,message):
    try:
        context.message = context.response.json()["message"]
        log.info(f'<{context.testcase_id}> - Actule tactic id : {context.tactic_id}')
        assert message == context.message, \
            log.exception(
                f'<{context.testcase_id}> - Actule message is  ({context.message}'
                f' does not matches Expected message)')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e