*DECK ZEXP
      SUBROUTINE ZEXP (AR, AI, BR, BI)
C***BEGIN PROLOGUE  ZEXP
C***SUBSIDIARY
C***PURPOSE  Subsidiary to ZBESH, ZBESI, ZBESJ, ZBESK, ZBESY, ZAIRY and
C            ZBIRY
C***LIBRARY   SLATEC
C***TYPE      ALL (ZEXP-A)
C***AUTHOR  Amos, D. E., (SNL)
C***DESCRIPTION
C
C     DOUBLE PRECISION COMPLEX EXPONENTIAL FUNCTION B=EXP(A)
C
C***SEE ALSO  ZAIRY, ZBESH, ZBESI, ZBESJ, ZBESK, ZBESY, ZBIRY
C***ROUTINES CALLED  (NONE)
C***REVISION HISTORY  (YYMMDD)
C   830501  DATE WRITTEN
C   910415  Prologue converted to Version 4.0 format.  (BAB)
C***END PROLOGUE  ZEXP
      DOUBLE PRECISION AR, AI, BR, BI, ZM, CA, CB
C***FIRST EXECUTABLE STATEMENT  ZEXP
      ZM = EXP(AR)
      CA = ZM*COS(AI)
      CB = ZM*SIN(AI)
      BR = CA
      BI = CB
      RETURN
      END
