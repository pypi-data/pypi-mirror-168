import typer
import beginai as bg
from uuid import UUID
from rich import print

app = typer.Typer()

@app.command(name="process_user_data")
def process_user_data(app_id: UUID = typer.Option(...), 
                    license_key: str = typer.Option(...), 
                    csv_file_location: str = typer.Option(...), 
                    column_representing_user_id: str = typer.Option(...),
                    column_representing_label: str = None, 
                    file_separator: str = ',',
                    host: str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(str(app_id), license_key, host)
        embeddings_applier.load_user_data(csv_file_location, column_representing_user_id, label_column=column_representing_label, file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)

@app.command(name="process_object_data")
def process_object_data(app_id: UUID = typer.Option(...), 
                    license_key: str = typer.Option(...), 
                    csv_file_location: str = typer.Option(...), 
                    object_name: str = typer.Option(...), 
                    column_representing_object_id: str = typer.Option(...),
                    column_representing_label: str = None, 
                    file_separator: str = ',',
                    host:str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(str(app_id), license_key, host)
        embeddings_applier.load_object_data(csv_file_location, object_name, column_representing_object_id,label_column=column_representing_label, file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)


@app.command(name="process_interactions")
def process_interactions(app_id: UUID = typer.Option(...), 
                    license_key: str = typer.Option(...), 
                    csv_file_location: str = typer.Option(...), 
                    column_representing_user_id: str = typer.Option(...),
                    object_name: str = typer.Option(...),
                    column_representing_object_id: str = typer.Option(...),
                    column_representing_action: str =  typer.Option(...), 
                    file_separator: str = ',',
                    host:str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(str(app_id), license_key, host)
        embeddings_applier.load_interactions(csv_file_location, column_representing_user_id, object_name, column_representing_object_id, column_representing_action, file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)

if __name__ == "__main__":
    app()

