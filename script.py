def save_data(app):
    app.Window_(best_match='Многоканальныйосциллограф', top_level_only=True).\
        child_window(title="Запись", auto_id="1016", control_type="Button").click()
    # sleep(0.5)
    app.Dialog2.СохранитьButton.click()
