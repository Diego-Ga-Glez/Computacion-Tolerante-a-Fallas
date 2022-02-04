while True:
    try:
        var = int(input("Digite un numero entero entre 0 y 10: "))

        if var < 0:
            assert False
        elif var > 10:
            raise Exception
        
    except ValueError:
        print("\nLa entrada no es un numero entero :(")
    except AssertionError:
        print("\nNumero menor a 0")
    except Exception:
        print("\nNumero mayor a 10")

    else:
        print("\nLa entrada es un numero entre 0 y 10")
    finally:
        print("\nFin del script\n")