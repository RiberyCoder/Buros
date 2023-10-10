Sub Formatea()
Dim a As String
    a = Range("G28").Value
    a = Replace(a, "---", Chr(10))
    Range("G28").Value = a
    Rows("28:28").EntireRow.AutoFit
End Sub
