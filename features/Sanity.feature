Feature: Performance optimization sanity test suite

  Background:
        Given I set base REST API url and headers correctly
        Given Set csv path to data/Sanity test cases.csv

        Scenario: Verify the response of the "tacticvalidation" API.
        Given Execute test case po_sanity 01
        When I set api endpoint to tactic_validation
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And Validate success from csv

        Scenario: Verify the response for creating a tactic, performing on/off operation and verifying on the overview
        page.
        Given Execute test case po_sanity 02
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And Validate success from csv
        When I set api endpoint to tactic_overview
          And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
            And Validate if tactic status is on on overview
        Given Set tactic status to off
        When I set api endpoint to tactic_on_off
          And Set the body of request to blank
          And Perform put
        Then Validate HTTP response code
            And Validate error from csv
        When I set api endpoint to tactic_overview
          And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
            And Validate if tactic status is off on overview
        Given Set tactic status to on
        When I set api endpoint to tactic_on_off
          And Set the body of request to blank
          And Perform put
        Then Validate HTTP response code
            And Validate error from csv
        When I set api endpoint to tactic_overview
          And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
            And Validate if tactic status is on on overview
            And Delete the tactic

        Scenario: Validate Get tactic data API.
        Given Execute test case po_sanity 03
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And Validate success true
        When I set api endpoint to get_tactic_data
            And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from get request
            And Delete the tactic

        Scenario: Validate Get tactic data API update.
        Given Execute test case po_sanity 04
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And Validate success true
        When I set api endpoint to create_tactic
            And Set the body of request to update body
            And Perform put
        Then Validate HTTP response code
            And Validate error from csv
            And Validate success true

        Scenario: Validate all the "filtergroups" APIs.
        Given Execute test case po_sanity 07
        When I set level to campaign
            And I set api endpoint to create_filtergroups
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
        When I set api endpoint to get_filtergroups
          And Perform get
        Then Validate HTTP response code
          And Validate error from csv
          And Validate if filtergroups Id is present from post
          And Validate if filtergroups filter_name is present from post
        When I set api endpoint to delete_filtergroups
          And Perform delete
        Then Validate HTTP response code
          And Validate error from csv
        Then Validate HTTP response code
            And Validate error from csv
        When I set api endpoint to get_filtergroups
          And Perform get
        Then Validate HTTP response code
          And Validate error from csv
          And Validate if filtergroups Id is not present from post

        Scenario: Validate the response of the "tasks" api.
        Given Execute test case po_sanity 08
          And Set tactic id to 25997 and task id to 72915
        When I set api endpoint to task_overview
          And Perform get
        Then Validate HTTP response code
          And Validate error from csv
          And Validate if applied_to is 1 Ad on task overview
          And Validate if task_checked_status is Rule starts checking at 23:30 IST on task overview

        Scenario: Validate the response of the "logs" api for the last execution.
        Given Execute test case po_sanity 09
          And Set tactic id to 25978 and task id to 72824
        When I set api endpoint to task_logs
          And Perform get
        Then Validate HTTP response code
          And Validate error from csv
          And Validate if rule_results is 1 campaign changed for Add To Name on task logs
          And Validate if changed is 1 campaign changed on task logs
        When I set api endpoint to datelogs
          And Perform get
        Then Validate HTTP response code
          And Validate error from csv
          And Validate if concept_id is 23845511455630083 on task datelogs
          And Validate if concept_name is FB_Pyxis_Social_Objective:Conversions_StoryID:*AQ-PYSO-STRIAL-0820-01*_AUG_TEST20_Term1:Start-Trial_Term2:_US_TG2test_Text_Test 1_new test on task datelogs
          And Validate if details is Text added, previous name was FB_Pyxis_Social_Objective:Conversions_StoryID:*AQ-PYSO-STRIAL-0820-01*_AUG_TEST20_Term1:Start-Trial_Term2:_US_TG2test_Text_Test 1 on task datelogs

        # @Sim
        Scenario:  Validate Tactic overview page API
        Given Execute test case po_sanity 05
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And validate Success True
        When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
            And validate pages
            And validate page_size
            And Validate current_page
            And Validate total count of tactic on overview
            And Delete the tactic

#    create the tactic check on task overview page
#     Delete the tactic and again check on task overview
  Scenario:  Validate Delete tactic API
        Given Execute test case po_sanity 06
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And validate Success True

        When I set api endpoint to get_tactic_data
            And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from task getRequest

        Given Execute test case po_sanity 06
        When I set api endpoint to delete_tactic
            And Perform delete
        Then Validate HTTP response code
            And Validate error from csv
            And validate success True

        When I set api endpoint to task_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error true
            And Validate message Tactic not found

    #Create the tactic and validate the response
    #Update the tactic and again validate the get response.[perticular updated parameter]
  Scenario:  Validate Update tactic data API
        Given Execute test case po_sanity 04
        When I set api endpoint to create_tactic
            And Set the body of request to body
            And Perform post
        Then Validate HTTP response code
            And Validate error from csv
            And validate Success from csv

       When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
#            And Validate name

        Given Execute test case po_sanity 04
        When I set api endpoint to update_tactic
            And Set the body of request to Update body
            And Perform put
        Then Validate HTTP response code
            And Validate error from csv
            And validate Success from csv

        When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error from csv
            And Validate tactic id from overview
#            And Validate name