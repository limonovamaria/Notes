import datetime
import fastapi
from src.model import CreateNote, Note, UpdateNote, GetNoteInfo, DeleteNote, GetNotesList, GetNoteText

api_router = fastapi.APIRouter()

listOfNotes = []
listOfId = {}
index = 0

@api_router.get("/getNoteText", response_model=GetNoteText)
def getNoteText(id: int, token:str):
    readNotes("notes.txt")
    if (isTrueToken(token)):
        for note in listOfNotes:
            if int(note.note_id) == id:
                return GetNoteText(id = note.note_id, text = note.text)
        return GetNoteText(id=-1, text="id not found")
    return GetNoteText(id=-1, text="false token")

def readNotes(fileName):
    global listOfNotes, listOfId, index
    listOfNotes.clear()
    with open(fileName, "r") as file:
        for line in file:
            noteMas = line.split(" ")
            print(noteMas)
            date_time_obj1 = datetime.datetime.strptime(noteMas[2]+ " " + noteMas[3], '%Y-%m-%d %H:%M:%S.%f')
            date_time_obj2 = datetime.datetime.strptime(noteMas[4]+ " " + noteMas[5][:len(noteMas[5])-1], '%Y-%m-%d %H:%M:%S.%f')
            note = Note(int(noteMas[0]), noteMas[1], date_time_obj1, date_time_obj2)
            listOfNotes.append(note)
            if (note.note_id not in listOfId.values()):
                listOfId[index] = note.note_id
                index+=1

def isTrueToken(token):
    tokens = []
    with open("tokens.txt", "r") as file:
        for line in file:
            if (line[len(line)-1]=='\n'):
                tokens.append(line[:len(line)-1])
            else:
                tokens.append(line)
        if (token in tokens):
            return True
    return False

@api_router.post("/createNote", response_model=CreateNote)
def createNote(text:str, token:str):
    readNotes("notes.txt")
    ID = 1
    if (len(listOfNotes)>1):
        for i in range(len(listOfId)):
            if ID in listOfId.values():
                ID+=1
    isToken = isTrueToken(token)
    if (isToken):
        note = Note(ID, text, datetime.datetime.now(), datetime.datetime.now())
        with open("notes.txt", "a+") as new_file:
            new_file.write(str(note.note_id) + " " + note.text + " " + str(note.created_time) + " " + str(note.updated_time) + "\n")
        return CreateNote(id=note.note_id)
    return GetNoteText(id=-1, text="false token")

@api_router.patch("/updateNote", response_model=UpdateNote)
def updateNote(note_id: int, text:str, token:str):
    readNotes("notes.txt")
    isToken = isTrueToken(token)
    if (isToken):
        updated_note = None
        file = open("notes.txt", "w")
        print(listOfNotes)
        for note in listOfNotes:
            if int(note.note_id) == note_id:
                note.update(text, datetime.datetime.now())
                updated_note = note
            file.write(str(note.note_id) + " " + note.text + " " + str(note.created_time) + " " + str(note.updated_time) + "\n")

        if (updated_note!=None):
            return UpdateNote(id=updated_note.note_id, text=updated_note.text)
        return UpdateNote(id = -1, text = "id not found")
    return UpdateNote(id=-1, text="false token")

@api_router.get("/getNoteInfo",response_model=GetNoteInfo)
def getNoteInfo(note_id: int, token:str):
    readNotes("notes.txt")
    isToken = isTrueToken(token)
    if (isToken):
        for note in listOfNotes:
            if int(note.note_id) == note_id:
                print(note.created_time)
                print(note.updated_time)
                return GetNoteInfo(created_at = note.created_time, updated_at = note.updated_time)
    return GetNoteText(id=-1, text="false token")

@api_router.delete("/removeNote",response_model=DeleteNote)
def removeNote(note_id : int, token:str):
    global  index, listOfId
    readNotes("notes.txt")
    isToken = isTrueToken(token)
    file = open("notes.txt", "w")
    if (isToken):
        for i in listOfId.keys():
            if listOfId[i] == note_id:
                deleted_note = listOfId[i]
                listOfId.pop(i)
                listOfNotes.pop(i)
                newList = {}
                for j in range(len(listOfId.keys())):
                    if (j>=i):
                        newList[j] = listOfId[j+1]
                    else:
                        newList[j] = listOfId[j]
                listOfId = newList
                index -= 1
                break
        for note in listOfNotes:
            file.write(str(note.note_id) + " " + note.text + " " + str(note.created_time) + " " + str(note.updated_time) + "\n" )
        return DeleteNote(removed_id = deleted_note)
    return GetNoteText(id=-1, text="false token")

@api_router.get("/getNotesList",response_model=GetNotesList)
def getNotesList(token:str):
    readNotes("notes.txt")
    if (isTrueToken(token)):
        return GetNotesList(notes_list = listOfId)
    return GetNoteText(id=-1, text="false token")

