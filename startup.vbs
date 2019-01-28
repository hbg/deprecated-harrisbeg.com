Set cmd = CreateObject("WScript.shell")

cmd.run"cmd"
WScript.sleep 200
cmd.Sendkeys"cd  C:\Users\legos\OneDrive\Desktop\Main\Flask\{Enter}"
WScript.sleep 200
cmd.Sendkeys"python app{Enter}"
WScript.sleep 200
