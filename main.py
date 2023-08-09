import json
import os
from datetime import datetime

class Note:
    def __init__(self, id, title, body, created_at, updated_at):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at

class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for note_data in data:
                    note = Note(**note_data)
                    self.notes.append(note)

    def save_notes(self):
        with open(self.file_path, 'w') as file:
            data = [{'id': note.id,
                     'title': note.title,
                     'body': note.body,
                     'created_at': note.created_at,
                     'updated_at': note.updated_at}
                    for note in self.notes]
            json.dump(data, file)

    def add_note(self, title, body):
        now = datetime.now()
        note = Note(id=len(self.notes) + 1, title=title, body=body,
                    created_at=now.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=now.strftime('%Y-%m-%d %H:%M:%S'))
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, new_title, new_body):
        for note in self.notes:
            if note.id == note_id:
                note.title = new_title
                note.body = new_body
                note.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def list_notes(self, filter_date=None):
        if filter_date:
            filtered_notes = [note for note in self.notes if note.created_at[:10] == filter_date]
        else:
            filtered_notes = self.notes

        for note in filtered_notes:
            print(f"ID: {note.id}")
            print(f"Title: {note.title}")
            print(f"Body: {note.body}")
            print(f"Created At: {note.created_at}")
            print(f"Updated At: {note.updated_at}")
            print("=" * 30)

if __name__ == "__main__":
    notes_manager = NoteManager("notes.json")

    while True:
        print("Commands:")
        print("add - Add a new note")
        print("edit - Edit an existing note")
        print("delete - Delete a note")
        print("list - List all notes")
        print("exit - Exit the application")

        command = input("Enter command: ")

        if command == "add":
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            notes_manager.add_note(title, body)
            print("Note added successfully!")

        elif command == "edit":
            note_id = int(input("Enter note ID to edit: "))
            new_title = input("Enter new title: ")
            new_body = input("Enter new body: ")
            if notes_manager.edit_note(note_id, new_title, new_body):
                print("Note edited successfully!")
            else:
                print("Note not found!")

        elif command == "delete":
            note_id = int(input("Enter note ID to delete: "))
            notes_manager.delete_note(note_id)
            print("Note deleted successfully!")

        elif command == "list":
            filter_date = input("Enter date to filter (YYYY-MM-DD) or press Enter for all notes: ")
            notes_manager.list_notes(filter_date)

        elif command == "exit":
            break

        else:
            print("Invalid command. Please try again.")
