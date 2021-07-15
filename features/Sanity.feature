Feature: Tactic creation Step 1 API testing

  Background:
        Given I set base REST API url and headers correctly
        Given Set csv path to data/Sanity test cases.csv
  @smoke
  Scenario:  Validate Tactic overview page API
        Given Execute test case po_sanity 02
        When I set api endpoint to create_tactic
            And Set the body of request
            And Perform post
        Then Validate HTTP response code
            And Validate error
            And validate Success
        When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error
            And Validate tactic id from overview
            And validate pages
            And validate page_size
            And Validate current_page
            And Validate total count of tactic on overview
            And Delete the tactic

#    create the tactic check on task overview page
#     Delete the tactic and again check on task overview
  Scenario:  Validate Delete tactic API
        Given Execute test case po_sanity 02
        When I set api endpoint to create_tactic
            And Set the body of request
            And Perform post
        Then Validate HTTP response code
            And Validate error
            And validate Success

        When I set api endpoint to task_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error
            And Validate tactic id from task overview

        Given Execute test case po_sanity 06
        When I set api endpoint to delete_tactic
            And Perform delete
        Then Validate HTTP response code
            And Validate error
            And validate Success

        When I set api endpoint to task_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error
            And Validate massage

    #Create the tactic and validate the response
    #Update the tactic and again validate the get response.[perticular updated parameter]
  Scenario:  Validate Update tactic data API
        Given Execute test case po_sanity 02
        When I set api endpoint to create_tactic
            And Set the body of request
            And Perform post
        Then Validate HTTP response code
            And Validate error
            And validate Success

       When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error
            And Validate tactic id from overview
            And Validate the name

        Given Execute test case po_sanity 04
        When I set api endpoint to update_tactic
            And Set the body of request
            And Perform put
        Then Validate HTTP response code
            And Validate error
            And validate Success

        When I set api endpoint to tactic_overview
            And Perform get
        Then Validate HTTP response code
            And Validate error
            And Validate tactic id from overview
            And Validate the name

