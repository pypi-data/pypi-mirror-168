from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509
from cryptography.hazmat.primitives import hashes

import datetime

class ServerLocationInfo():
    def __init__(self, country: str, state: str, city: str) -> None:
        self.country = country
        self.state = state
        self.city = city

class Ssl():
    def __init__(self, pubkey_name: str = None, privkey_name: str = None) -> None:
        self.PUBLIC_KEY_NAME = 'cert.pem' if pubkey_name == None else pubkey_name
        self.PRIVATE_KEY_NAME = 'priv.key' if privkey_name == None else privkey_name

    def generate_certificate(self, public_ip: str, bot_name: str, location: ServerLocationInfo):
        # Generate our key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Write our key to disk for safe keeping
        with open(self.PRIVATE_KEY_NAME, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
                # encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase_of_your_choice"),
            ))
        

        # Various details about who we are. For a self-signed certificate the
        # subject and issuer are always the same.
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, location.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, location.state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, location.city),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, bot_name),
            x509.NameAttribute(NameOID.COMMON_NAME, public_ip),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 30 days
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).add_extension(
            x509.SubjectAlternativeName([
                # Describe what sites we want this certificate for.
                # x509.DNSName(u"localhost"),
                x509.DNSName(public_ip),
            ]),
            # x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        # Sign our certificate with our private key
        ).sign(key, hashes.SHA256())
        # Write our certificate out to disk.
        with open(self.PUBLIC_KEY_NAME, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    @property
    def pubkey_bytes(self) -> bytes:
        try:
            with open(self.PUBLIC_KEY_NAME, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'Could not find public certificate file named: {self.PUBLIC_KEY_NAME}.')
