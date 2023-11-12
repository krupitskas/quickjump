import N10X
import re
 
g_StillSearching = False
g_ActiveWord = ""
g_ActiveWordDuplicateNumber = 0 # We can match multiple similar words, so we should iterate over position between them
g_MaxWordDuplicateNumber = 0
g_WordPosJumpMap = dict()

def StopQuickJumpSearch():
    global g_StillSearching
    global g_ActiveWord
    global g_ActiveWordDuplicateNumber
    global g_MaxWordDuplicateNumber
    global g_WordPosJumpMap

    g_StillSearching = False
    activeWord = ""
    N10X.Editor.ResetCursorMode()
    N10X.Editor.ClearCursorColourOverride()
    N10X.Editor.SetStatusBarText("")
    
    N10X.Editor.RemoveOnInterceptKeyFunction(HandleCommandModeKey)
    N10X.Editor.RemoveOnInterceptCharKeyFunction(WordSearchUpdate)
    N10X.Editor.RemoveUpdateFunction(UpdateStatusBar)
    
    g_ActiveWord = ""
    g_WordPosJumpMap = dict()
    g_ActiveWordDuplicateNumber = 0
    g_MaxWordDuplicateNumber = 0

# Create a dictionary of words
def StartQuickJumpSearch():
    global g_StillSearching
    global g_WordPosJumpMap
    
    g_WordPosJumpMap = {}
    
    startLineNum = N10X.Editor.GetScrollLine()
    
    for lineOffset in range(N10X.Editor.GetVisibleLineCount()):
        currentLineNum = startLineNum + lineOffset
        currentLineText = str(N10X.Editor.GetLine(currentLineNum))
        textSplitArray = SplitText(currentLineText)
        
        for wordPosition in textSplitArray:
            word = wordPosition[0]
            x = wordPosition[1]
            y = currentLineNum
        
            if word not in g_WordPosJumpMap:
                g_WordPosJumpMap[word] = [(x,y)]
            else:
                g_WordPosJumpMap[word].append((x,y))
            
    #g_StillSearching = True
    #N10X.Editor.SetCursorColourOverride((255,255,0))
    #N10X.Editor.SetCursorMode("Underscore")

def HandleCommandModeKey(key, shift, control, alt):
    global g_ActiveWord
    global g_ActiveWordDuplicateNumber
    global g_MaxWordDuplicateNumber
    
    # Iterate over duplicates
    if N10X.Editor.ControlKeyHeld():
        print("ass")
    
        if key == 'j':
            print("Down")
            g_ActiveWordDuplicateNumber += 1
            g_ActiveWordDuplicateNumber = 0 if g_ActiveWordDuplicateNumber > g_MaxWordDuplicateNumber else g_ActiveWordDuplicateNumber
            return True
        elif key == 'k':
            print("Up")
            g_ActiveWordDuplicateNumber -= 1
            g_ActiveWordDuplicateNumber = g_MaxWordDuplicateNumber if g_ActiveWordDuplicateNumber < 0 else g_ActiveWordDuplicateNumber
            return True
    
    if key == "Escape":
        StopQuickJumpSearch()
    if key == "Backspace":
        g_ActiveWord = g_ActiveWord[:-1]
    return True
        
def WordSearchUpdate(c):
    global g_ActiveWord
    global g_WordPosJumpMap
    global g_ActiveWordDuplicateNumber
    
    g_ActiveWord += c
    
    for key in g_WordPosJumpMap:
        if key.startswith(g_ActiveWord):        
            N10X.Editor.ClearCursorColourOverride()
            N10X.Editor.SetCursorPos(g_WordPosJumpMap[key][g_ActiveWordDuplicateNumber])
            g_MaxWordDuplicateNumber = len(g_WordPosJumpMap[key])
            return True
        else:
            N10X.Editor.SetCursorColourOverride((255,0,0))
    
    return True
    
def UpdateStatusBar():
    N10X.Editor.SetStatusBarText("Searching word: " + g_ActiveWord)
    
def SplitText(text):
    words = []
    word = ""
    pos = 0
    for char in text:
        if not char.isalnum():
            if word:
                words.append((word, pos))
                word = ""
            pos += 1
        else:
            if not word:
                pos = text.index(char)
            word += char
    if word:
        words.append((word, pos))
    return words

def HelloQuickJump():
    StartQuickJumpSearch()
    N10X.Editor.AddOnInterceptCharKeyFunction(WordSearchUpdate)
    N10X.Editor.AddOnInterceptKeyFunction(HandleCommandModeKey)
    N10X.Editor.AddUpdateFunction(UpdateStatusBar)