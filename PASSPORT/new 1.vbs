Option Explicit

dim ruta_print_job
ruta_print_job="C:\AD\PROCONTA\archivos\tempsintesis\PrintJob.txt"

msgbox(Revisar())


Function Revisar()
	Dim objFSO, objFile
	Set objFSO = CreateObject("Scripting.FileSystemObject")
	Set objFile = objFSO.GetFile(ruta_print_job)
	Revisar = objFile.Size
	Set objFile = Nothing
	Set objFSO = Nothing
End Function



function busca_saldo_disponible()
	busca_saldo_disponible=false
	dim fso111
	dim filename
	dim listFile
	dim listLines
	'dim procesado
	dim line, line2
	dim contenido
	Set fso111=CreateObject("Scripting.FileSystemObject")
	listFile = fso111.OpenTextFile(ruta_print_job).ReadAll
	contenido=Instr(listFile,"/table")
	if contenido>0 then
		busca_saldo_disponible=true
	end if		
End function