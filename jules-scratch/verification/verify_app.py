from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the main page
    page.goto("http://127.0.0.1:5001/")
    page.screenshot(path="jules-scratch/verification/01_main_page.png")

    # Click on the first chapter
    page.get_by_role("link", name="Aventuras e Narrativa").click()
    page.wait_for_load_state("networkidle")
    page.screenshot(path="jules-scratch/verification/02_chapter_page.png")

    # Click on the edit button
    page.get_by_role("link", name="Editar Capítulo").click()
    page.wait_for_load_state("networkidle")
    page.screenshot(path="jules-scratch/verification/03_edit_page.png")

    # Test template insertion
    initial_content = page.input_value("#editor")
    page.get_by_role("button", name="Caixa de Texto").click()

    # Add a small delay to ensure the event loop has time to process the click
    page.wait_for_timeout(200)

    new_content = page.input_value("#editor")

    # A unique part of the template to check for
    expected_text_snippet = "*Conteúdo da caixa...*"

    print("----- DEBUGGING -----")
    print(f"Expected to find snippet: '{expected_text_snippet}'")
    print(f"Actual content length: {len(new_content)}")
    print("---------------------")

    assert expected_text_snippet in new_content
    # Check that the new content is longer than the initial content
    assert len(new_content) > len(initial_content)

    print("Template insertion test passed!")
    page.screenshot(path="jules-scratch/verification/04_edit_page_with_template.png")

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
