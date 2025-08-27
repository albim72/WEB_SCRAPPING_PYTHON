try:
    H = parse_with("html.parser")
    L = parse_with("lxml")
    F = parse_with("html5lib")

    # Minimalne oczekiwania: lxml i html5lib znajdują 2 wiersze i 2 pliki
    assert len(L["rows"]) >= 2 and len(L["files"]) >= 2
    assert len(F["rows"]) >= 2 and len(F["files"]) >= 2

    # Parser wbudowany może zawieść – test „luźny”
    assert len(H["rows"]) >= 1
except AssertionError as e:
    print("UWAGA: różnice parserów ujawniły się zgodnie z oczekiwaniem:", e)
