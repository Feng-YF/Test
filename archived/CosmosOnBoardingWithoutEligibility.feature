@Cosmos @OnBoarding
Feature: On-boarding without eligible products

  @Cosmos-us @test
  Scenario: Go to Cosmos On-Boarding Terms and Conditions screen with unregistered account
    Given the OnlyCard user logs in with valid username and password to accounts summary
    And the user clicks the Global Money button
    And the user should be directed to OnBoarding Landing screen
    And the user clicks Next button on On-Boarding Landing 3 times
    And the user clicks Get Started button
    Then the user should see message about product not eligible