Feature: Tactic creation Step 1 API testing

  Background:
        Given I set base REST API url and headers correctly
  @smoke
  Scenario: API Create tactic
        Given Execute test case po_01
        When I set api endpoint to create_tactic endpoint
            And Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
        Then Extract tactic Id
            And Delete the tactic


  Scenario Outline: API Create tactic: Validate if "status" accepts <status>
        Given Execute test case <test_case>
        When I set api endpoint to create_tactic endpoint
            And Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
        Then Validate the status
            And Delete the tactic
        Examples:
          | test_case | status |
          | po_02     |  draft |
          | po_03     |  on    |
          | po_04     |  off   |
          | po_05     | null   |
          | po_06     | xyz    |
          | po_07     | 123    |


  Scenario Outline: API Create tactic: Validate if "date_schedule" accepts <date_schedule>
        Given Execute test case <test_case>
        When I set api endpoint to create_tactic endpoint
            And Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
        Then Validate the date_schedule
            And Delete the tactic
        Examples:
          | test_case | date_schedule |
          | po_08     |  continuously |
          | po_09     |  between_dates|

    Scenario Outline: API Create tactic: Validate if <date> accepts <input_date>
        Given Execute test case <test_case>
        When I set api endpoint to tactic_validation endpoint
            And Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
        Then Validate the <date>
            And Delete the tactic
        Examples:
          | test_case | input_date  | date      |
          | po_10     |  2021-05-15 | start_date|
          | po_11     |  2021-05-15 | end_date  |



