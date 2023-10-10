Option explicit
dim rutaresultados
rutaresultados="C:\AD\PROMUJER\CUADRESERV\archivos\Agencias\"

dim age
age="EJEMPL. AGENCIA VPP"

dim archivo
archivo="SUP_938056_31082020"
'archivo="XXXXX"

dim fecha
fecha="31082020"

'call Escriberesultado(rutaresultados,age, archivo)
msgbox( VerificaSolicitudesPrevias (archivo))

sub Escriberesultado(byref ruta_archivo, byref agencia, byref archivo )
	dim fso, existe
    Set fso = CreateObject ( "Scripting.FileSystemObject")
	
	if fso.FolderExists(ruta_archivo & "\" & agencia) = False  then
		fso.CreateFolder(ruta_archivo & "\" & agencia)
	end if
	
	
	if fso.FileExists(ruta_archivo & "\" & agencia & "\" & archivo & ".txt" ) = False  then
		fso.CreateTextFile(ruta_archivo & "\" & agencia & "\" & archivo & ".txt")
	end if
	
	
	dim a12
	set a12=fso.OpenTextFile(ruta_archivo & "\" & agencia & "\" & archivo & ".txt",8,true)
	a12.WriteLine(trim(age))
	a12.Close

	set fso=nothing
end Sub

Function VerificaSolicitudesPrevias (byref archivo2)
	dim objFSO, objFolder, colFiles, objFile
	VerificaSolicitudesPrevias=False
 
	Set objFSO = CreateObject("Scripting.FileSystemObject")
	Set objFolder = objFSO.GetFolder(rutaresultados & age & "\" & fecha  )
	Set colFiles = objFolder.Files
	
	For Each objFile in colFiles
		'msgbox(InStr (objFile , archivo2))
		if (InStr (objFile , archivo2)) > 0 then
			VerificaSolicitudesPrevias=True 
			Exit For
		end if
	Next
	
	set objFSO=nothing
	set colFiles=nothing
	set colFiles=nothing
end function