Feature: Interactive knowledge graph viewer
  As a visitor exploring the wiki
  I want the graph page to load, navigate, and gracefully handle nodes
  without compiled pages
  So I can trust clicks never land on a 404

  Background:
    Given a built llmwiki site is served

  Scenario: Graph viewer loads and renders nodes
    When I visit the graph page
    Then the graph canvas is visible
    And the stats overlay shows the page count

  Scenario: Graph viewer has back-to-site link
    When I visit the graph page
    Then the "Home" back-link is visible

  Scenario: Graph click handler reads site_url (no JS rewrite race)
    When I visit the graph page
    Then the graph JSON payload contains "site_url"
