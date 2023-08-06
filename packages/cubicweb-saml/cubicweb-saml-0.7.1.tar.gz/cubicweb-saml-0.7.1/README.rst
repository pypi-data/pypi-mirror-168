Cubicweb-SAML
=============
SAML2 authentifier for cubicweb. This cube allow to authenticate from a SAML2
provider with cubicweb login form.

Installation
------------
The first step is to install cubicweb-saml into your python environment:
::

    pip install cubicweb-saml

To add this cube into your cubicweb instance:
::

    cubicweb-ctl shell <your_app>
    >>> add_cube('saml')
    >>> exit

To generate SAML related option in all-in-one.conf:
::

    cubicweb-ctl upgrade <your_app>

Configuration
-------------
To configure cubicweb-saml metadata, open ``sources.conf`` from cubicweb
instances folder (by default ``$HOME/etc/cubicweb.d/<instance>``):
::

    [SAML]

    # SAML v2 metadata uri which can be read from a file (file://<absolute_path>)
    # or retrieved from a specific URL(http[s]://...)
    saml-metadata-uri=

    # The globally unique identifier of the entity.
    saml-entity-id=

To configure cubicweb-saml options, open ``all-in-one.conf`` in the same
directory:
::

    [SAML]

    # Don't verify that the incoming requests originate from us via the built-in
    # cache for authn request ids in pysaml2
    saml-allow-unsolicited=yes

    # Indicates if the Authentication Requests sent by this SP should be signed by
    # default.
    saml-authn-requests-signed=no

    # Indicates if this entity will sign the Logout Requests originated from it.
    saml-logout-requests-signed=yes

    # Indicates if this SP wants the IdP to send the assertions signed. This sets
    # the WantAssertionsSigned attribute of the SPSSODescriptor node of the
    # metadata so the IdP will know this SP preference.
    saml-want-assertions-signed=yes

    # Indicates that Authentication Responses to this SP must be signed. If set to
    # True, the SP will not consume any SAML Responses that are not signed.
    saml-want-response-signed=no

    # Allow to register a new user
    # if this one does not exist in current database.
    saml-register-unknown-user=no

    # Set the default group to register new user
    # if the saml-register-unknown-user option was activated.
    saml-register-default-group=guests

    # Set the default password system to use if the saml-register-unknown-user
    # option was activated (available values: empty, random).
    saml-register-default-password=empty
