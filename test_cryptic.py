import cryptic


crpt = cryptic.Cryptic("UserName", "Password")

def test_bxor():
    val1 = b'.\x19\x13\x84Z\x89^O\xb6\x80i\xfd\xbb]C\xccmW\x07\x8fB\xf2\x89\x93\x90#&W-u\x05\xda'
    val2 = b'\x81Y!\xabm\xe6~\x80l\xd8C\xa3\xe7\xff\x96q\x12&\xef\x8d\xb5]X5\x88\x14\x96\x96nV\xd2j'
    outcome = b'\xaf@2/7o \xcf\xdaX*^\\\xa2\xd5\xbd\x7fq\xe8\x02\xf7\xaf\xd1\xa6\x187\xb0\xc1C#\xd7\xb0'
    assert crpt.bxor(val1, val2) == outcome

def test_passkey():
    pin1 = 1256348
    pin2 = 2256348
    pin3 = 0
    pin4 = -1203455
    pin5 = "abc"
    # Default
    assert crpt.__passkey__(pin1) == crpt.__passkey__(pin1, True, 1)
    # Reproducibility
    assert crpt.__passkey__(pin1, True, 1) == crpt.__passkey__(pin1, True, 1)
    assert crpt.__passkey__(pin1, True, 10) == crpt.__passkey__(pin1, True, 10)
    assert crpt.__passkey__(pin1, False, 1) == crpt.__passkey__(pin1, False, 1)
    assert crpt.__passkey__(pin1, False, 10) == crpt.__passkey__(pin1, False, 10)
    # Salt check
    assert crpt.__passkey__(pin1, True, 1) != crpt.__passkey__(pin1, True, 2)
    # Node check
    assert crpt.__passkey__(pin1, True, 1) != crpt.__passkey__(pin1, False, 1)
    # Pin Check
    assert crpt.__passkey__(pin1, True, 1) != crpt.__passkey__(pin2, True, 1)
    # Corner cases
    assert crpt.__passkey__(pin3, True, 1) == crpt.__passkey__(pin3, True, 1)
    assert crpt.__passkey__(pin4, True, 1) == crpt.__passkey__(pin4, True, 1)
    assert crpt.__passkey__(pin4, True, 1) == 0
    assert crpt.__passkey__(pin5, True, 1) == 0
    assert crpt.__passkey__(pin1, True, 1) != crpt.__passkey__(pin3, True, 1)
    assert crpt.__passkey__(pin3, True, 1) != crpt.__passkey__(pin4, True, 1)

def test_crypt_aes_decrypt_aes():
    pin1 = 1256348
    pin2 = -256348
    pin3 = 1256349
    testword1 = 'Hi Hello'
    testword2 = b'.\x19\x13\x84Z\x89^O\xb6\x80i\xfd\xbb]C\xccmW\x07\x8fB\xf2\x89\x93\x90#&W-u'
    testword3 = bytes(testword1, 'utf-8')
    out_p1_t1_t1 = crpt.crypt_aes(testword1, pin1, True, 1)
    out_p3_t1_t1 = crpt.crypt_aes(testword1, pin3, True, 1)
    out_p1_t2_f1 = crpt.crypt_aes(testword2, pin1, False, 1)
    out_p1_t2_t1 = crpt.crypt_aes(testword2, pin1, True, 1)
    out_p2_t1_f1 = crpt.crypt_aes(testword1, pin2, False, 1)
    out_p2_t1_t8 = crpt.crypt_aes(testword1, pin2, True, 8)
    out_p1_t1_def = crpt.crypt_aes(testword1, pin1)
    out_p1_t3_t1 = crpt.crypt_aes(testword3, pin1, True, 1)
    # Check error
    assert out_p2_t1_f1 == 'error'
    assert out_p2_t1_t8 == 'error'
    # Check different result everytime
    assert out_p1_t1_t1 != out_p1_t1_def
    # Check decryption
    assert crpt.decrypt_aes(out_p1_t1_def, pin1) == testword1
    assert crpt.decrypt_aes(out_p1_t2_f1, pin1, False, 1) == testword2
    assert crpt.decrypt_aes(out_p1_t2_t1, pin1) == testword2
    assert crpt.decrypt_aes(out_p3_t1_t1, pin3) == testword1
    assert crpt.decrypt_aes(out_p1_t3_t1, pin1) == testword1
    # Check wrong pin
    assert crpt.decrypt_aes(out_p1_t3_t1, pin3) == out_p1_t3_t1
    assert crpt.decrypt_aes(out_p1_t3_t1, pin1, False, 1) == out_p1_t3_t1
    assert crpt.decrypt_aes(out_p1_t3_t1, pin1, True, 2) == out_p1_t3_t1
    # Check error
    assert crpt.decrypt_aes(testword1, pin1) == testword1
    assert crpt.decrypt_aes(out_p1_t3_t1, pin2) == out_p1_t3_t1