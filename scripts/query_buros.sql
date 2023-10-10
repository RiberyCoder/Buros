use buros
SELECT *from GRUPO g 
select *from GEO_VIVIENDA


DELETE FROM PERSONA
WHERE TIKET IN (SELECT TIKET FROM GRUPO WHERE tipo LIKE '%RECONSULTA%');

DELETE FROM GRUPO
WHERE tipo LIKE '%RECONSULTA%';

select top 1 N_SOLICITUD, ESTADO from SOLICITUD_PCCU    where  TICKET= 456324 and IDPERSONA=491295 order by N_SOLICITUD desc

SELECT
    G.usuario AS usuario,
    COUNT(*) AS cantidad_de_repeticiones
FROM GRUPO G
GROUP BY G.usuario;


SELECT
    G.usuario AS usuario,
    (SELECT TOP 1 CI
     FROM PERSONA
     GROUP BY CI
     ORDER BY COUNT(*) DESC) AS CI_mas_frecuente,
    COUNT(*) AS cantidad_de_repeticiones
FROM GRUPO G
GROUP BY G.usuario;

SELECT (*) FROM GRUPO g INNER JOIN 
SELECT DISTINCT usuario FROM GRUPO

SELECT P.TIKET, P.NOMBRE, P.PATERNO, P.MATERNO,G.usuario  FROM PERSONA P INNER JOIN GRUPO G ON P.TIKET = G.tiket WHERE G.usuario IN (SELECT DISTINCT usuario FROM GRUPO) 
ORDER BY G.usuario 

SELECT
    P.TIKET,
    P.NOMBRE,
    P.PATERNO,
    P.MATERNO,
    G.usuario AS USUARIO,
    COUNT(*) AS CANTIDAD_DE_REPETICIONES,
    P.TIPO
FROM PERSONA P
INNER JOIN GRUPO G ON P.TIKET = G.tiket
WHERE G.usuario IN (SELECT DISTINCT usuario FROM GRUPO) 
GROUP BY P.TIKET, P.NOMBRE, P.PATERNO, P.MATERNO,P.TIPO , G.usuario
--HAVING COUNT(*) > 2
ORDER BY G.usuario,cantidad_de_repeticiones DESC;


SELECT COUNT(*) AS cantidad_total_de_registros
FROM (
    SELECT
    P.TIKET,
    P.NOMBRE,
    P.PATERNO,
    P.MATERNO,
    G.usuario AS USUARIO,
    COUNT(*) AS CANTIDAD_DE_REPETICIONES,
    P.TIPO
FROM PERSONA P
INNER JOIN GRUPO G ON P.TIKET = G.tiket
WHERE G.usuario IN (SELECT DISTINCT usuario FROM GRUPO) 
GROUP BY P.TIKET, P.NOMBRE, P.PATERNO, P.MATERNO,P.TIPO , G.usuario
--HAVING COUNT(*) > 2
) AS subconsulta;


select * from PERSONA p WHERE TIKET  = '347623'

######################################################################
#			  CREACION DE UNA NUEVA TABLA							 #
######################################################################

CREATE TABLE RegistroAccesosInfocred (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Id_persona INT NOT NULL,
    Ingresos_servis INT DEFAULT 0
);


CREATE PROCEDURE ActualizarIngresosServis
ALTER PROCEDURE ActualizarIngresosServis
    @IdPersona INT
AS
BEGIN
    DECLARE @FechaActual DATETIME;
    SET @FechaActual = GETDATE(); -- Obtener la fecha y hora actual

    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'RegistroAccesosInfocred' AND COLUMN_NAME = 'FechaRegistro')
    BEGIN
        -- Si el campo "FechaRegistro" no existe, agrégalo a la tabla
        ALTER TABLE RegistroAccesosInfocred
        ADD FechaRegistro DATETIME;
    END

    IF NOT EXISTS (SELECT 1 FROM RegistroAccesosInfocred WHERE Id_persona = @IdPersona)
    BEGIN
        -- Inserta un nuevo registro con el campo "FechaRegistro"
        INSERT INTO RegistroAccesosInfocred (Id_persona, Ingresos_servis, FechaRegistro)
        VALUES (@IdPersona, 1, @FechaActual); -- Iniciar con 1 en Ingresos_servis y registrar la fecha actual
    END
    ELSE
    BEGIN
        -- Actualiza el registro existente y la fecha actual
        UPDATE RegistroAccesosInfocred
        SET Ingresos_servis = Ingresos_servis + 1,
            FechaUltimoRegistro = @FechaActual -- Actualizar la fecha actual
        WHERE Id_persona = @IdPersona;
    END
END;


ALTER TABLE RegistroAccesosInfocred
ADD FechaUltimoRegistro DATETIME;
ADD FechaRegistro DATETIME;

select * from RegistroAccesosInfocred
EXEC ActualizarIngresosServis 499827;

######################################################################
#			  QUERYS EXTRAS PARA EL USO 							 #
######################################################################


DELETE FROM [RegistroAccesosInfocred]
WHERE Id_persona <> '457023' AND Id_persona <> '457276';

-- Reiniciar el contador de autoincremento para la columna ID
DBCC CHECKIDENT ('RegistroAccesosInfocred', RESEED, 0);

SELECT * FROM SCORING

DELETE FROM SCORING;

DBCC CHECKIDENT (SCORING, RESEED, 0);
select estado from GRUPO where tipo  LIKE '%reconsulta-401973'

UPDATE GRUPO 
SET estado = 'PENDIENTE'
WHERE tipo LIKE '%reconsulta-401973';

SELECT * FROM GRUPO

select PERSONA.CI, PERSONA.TIPO,GRUPO.monto_buro from GRUPO inner join PERSONA on GRUPO.tiket=PERSONA.TIKET where grupo.TIKET= 401973
[dbo].[SP_SELECT_CONSULTA_PCCU]

DELETE FROM PERSONA
WHERE TIKET IN (SELECT TIKET FROM GRUPO WHERE tipo LIKE '%RECONSULTA%');

DELETE FROM GRUPO
WHERE tipo LIKE '%RECONSULTA%';

CREATE PROCEDURE [dbo].[SP_SELECT_CONSULTA_PCCU]
	 @TICKET INT 
AS
BEGIN
	DECLARE @TICKETSTRING VARCHAR(50) = CONVERT(VARCHAR(10), @TICKET)
	select PERSONA.TIKET, PERSONA.ID_PERSONA, PATERNO, MATERNO, AP_CASADA,NOMBRE, NOMBRE,CI, usuario, para_correo, agencia from persona
INNER JOIN GRUPO ON PERSONA.TIKET=GRUPO.tiket

where GRUPO.tipo LIKE '%'+@TICKETSTRING  

END;

EXEC [dbo].[SP_SELECT_CONSULTA_PCCU] 456632

UPDATE SOLICITUD  SET ESTADO='PENDIENTE' WHERE ID_SOLICITUD= (select top 1 ID_SOLICITUD from SOLICITUD  WHERE TICKET= 456624 order by ID_SOLICITUD desc)

SELECT * FROM SOLICITUD WHERE ID_SOLICITUD= (select top 1 ID_SOLICITUD from SOLICITUD  WHERE TICKET= 456624 order by ID_SOLICITUD desc)

select top 1 N_SOLICITUD, ESTADO from SOLICITUD_PCCU    where  TICKET= 456632 and IDPERSONA= 491611 order by N_SOLICITUD desc

UPDATE SOLICITUD  SET  RES_BUROS='ACEPTADO' WHERE TICKET= {ticket_ant}


EXECUTE SP_SELECT_COMPARAR_ASFI_INFOCRED_v2 @CI='{ci}', @TIKET1 =  {ticket_ant}, @TIKET2 = {ticket_db}

select GRUPO.tiPO,PERSONA.TIKET, PERSONA.ID_PERSONA, PATERNO, MATERNO, AP_CASADA,NOMBRE, NOMBRE,CI, usuario, para_correo, agencia from persona
INNER JOIN GRUPO ON PERSONA.TIKET=GRUPO.tiket
WHERE PERSONA.TIKET  LIKE '%456617%'
where GRUPO.tiPO LIKE '%456617%'

SELECT * FROM  GRUPO  where tiPO LIKE '%456617%'
SELECT * FROM  PERSONA  where TIKET = '456617'


ALTER PROCEDURE [dbo].[SP_SELECT_CONSULTA_PCCU]
	 @TICKET INT 
AS
BEGIN
	DECLARE @TICKETSTRING VARCHAR(50) = CONVERT(VARCHAR(10), @TICKET)
	select PERSONA.TIKET, PERSONA.ID_PERSONA, PATERNO, MATERNO, AP_CASADA,NOMBRE, NOMBRE,CI, usuario, para_correo, agencia from persona
INNER JOIN GRUPO ON PERSONA.TIKET=GRUPO.tiket

where GRUPO.tiPO LIKE '%'+@TICKETSTRING  +'%'

END

exec [dbo].[SP_SELECT_CONSULTA_PCCU] 456324
DECLARE @TICKET INT = 456617
DECLARE @TICKETSTRING VARCHAR(50) = CONVERT(VARCHAR(10), @TICKET)
SELECT @TICKETSTRING
	select PERSONA.TIKET, PERSONA.ID_PERSONA, PATERNO, MATERNO, AP_CASADA,NOMBRE, NOMBRE,CI, usuario, para_correo, agencia from persona
INNER JOIN GRUPO ON PERSONA.TIKET=GRUPO.tiket
WHERE PERSONA.TIKET LIKE '%'+@TICKETSTRING
--where GRUPO.tipo  LIKE '%'+@TICKETSTRING

ALTER PROCEDURE [dbo].[SP_SELECT_CONSULTA_PCCU]
	 @TICKET INT 
AS
BEGIN
	DECLARE @TICKETSTRING VARCHAR(50) = CONVERT(VARCHAR(10), @TICKET)
	select PERSONA.TIKET, PERSONA.ID_PERSONA, PATERNO, MATERNO, AP_CASADA,NOMBRE, NOMBRE,CI, usuario, para_correo, agencia from persona
INNER JOIN GRUPO ON PERSONA.TIKET=GRUPO.tiket

WHERE PERSONA.TIKET LIKE '%'+@TICKETSTRING

END


select id_persona,PERSONA.CI, PERSONA.TIPO,GRUPO.monto_buro from GRUPO inner join PERSONA on GRUPO.tiket=PERSONA.TIKET where grupo.TIKET=457750

select CI from ASFI_INFOCRED where tiket={ticket_ant} group by CI

CREATE PROCEDURE [dbo].[trae_pendiente]
AS
BEGIN
DECLARE @TICKET AS BIGINT 
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
    -- Insert statements for procedure here

	SET @TICKET = (SELECT top 1 [tiket]FROM [dbo].[GRUPO] WHERE [estado]='PENDIENTE' ) --and TIPO like 'RECONSULTA-%'
	--SET @TICKET = (SELECT top 1 [tiket]FROM [dbo].[GRUPO] WHERE tiket=580)-- and TIPO like 'RECONSULTA-%'  --580
	UPDATE [dbo].[GRUPO]  SET estado='EN_PROCESO' WHERE tiket=@TICKET 
	SELECT top 1 [tiket],[estado],[asunto],[tipo],[monto_buro],[para_correo], [id_solicitud] FROM [dbo].[GRUPO] WHERE tiket=@TICKET -- and TIPO like 'RECONSULTA-%'
END

EXEC [dbo].[trae_pendiente] /**00_EcofuturoAtiendeDB2**/

UPDATE [dbo].[GRUPO]  SET robot= 2 WHERE tiket= 456617 
select CI from ASFI_INFOCRED where tiket= 456617 group by CI --ComparativaCliente
select top 1 CI+CI_COM+' '+CI_EXT as CARNET, NOMBRE+' '+PATERNO+' '+MATERNO as NOMBRE from PERSONA where CI+CI_COM='460036' order by ID_PERSONA desc

ALTER PROCEDURE [dbo].[SP_SELECT_COMPARAR_ASFI_INFOCRED_FECHAS]
@CI VARCHAR(50),
@TIKET1 BIGINT,
@TIKET2 BIGINT

AS
BEGIN

SELECT [ASFI_PERIODO]
      ,[INFOCRED_ULT_F_ACT]  from ASFI_INFOCRED where TIKET = @TIKET1 and CI=@CI
UNION
SELECT [ASFI_PERIODO]
      ,[INFOCRED_ULT_F_ACT] FROM ASFI_INFOCRED WHERE TIKET	=@TIKET2 and CI=@CI
 	
END;
 EXECUTE SP_SELECT_COMPARAR_ASFI_INFOCRED_v2 @CI=7575407, @TIKET1 = 456149, @TIKET2 = 458153 --comparaData_testDB2
 
  
 SELECT TOP 1 para_correo FROM GRUPO WHERE tipo='RECONSULTA-456321' ORDER BY TIKET DESC
 select TOP 1 para_correo from GRUPO where tiket=456321 ORDER BY TIKET DESC
 select PERSONA.CI,PERSONA.NOMBRE, PERSONA.PATERNO, PERSONA.MATERNO  , PERSONA.TIPO,GRUPO.monto_buro from GRUPO inner join PERSONA on GRUPO.tiket=PERSONA.TIKET where grupo.TIKET=457338
 
 select CI from PERSONA where tipo='TITULAR' and tiket = 457224
 
EXECUTE SP_SELECT_COMPARAR_ASFI_INFOCRED_v2 @CI=4612900, @TIKET1 = 458291, @TIKET2 = 460036
 
EXECUTE SP_SELECT_COMPARAR_ASFI_INFOCRED_v2 @CI=4683686, @TIKET1 = 458291, @TIKET2 = 460036

BACKUP DATABASE BUROS 
TO DISK = 'C:\buros.bak'

