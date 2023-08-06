# copyright 2021-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__docformat__ = "restructuredtext en"

from pyramid.httpexceptions import HTTPSeeOther
from urllib.parse import urlparse

from cubicweb.predicates import anonymous_user
from cubicweb.tags import a
from cubicweb.web.views.basetemplates import LogInTemplate, LoggedOutTemplate

from cubicweb_saml.utils import retrieve_url_from_client


class SAMLLogMixin:
    """Mixin class used to manage log-related templates"""

    def get_saml_uri_from_request(self, request):
        """Retrieve the SAML URI based on receiving request

        Parameters
        ----------
        request : pyramid.request.Request
            Pyramid request used to retrieve SAML response

        Returns
        -------
        str
            SAML URI as string
        """

        return retrieve_url_from_client(self._cw.vreg.config, request)

    def on_activate_saml(self):
        """Retrieve and redirect to SAML URI"""

        uri = self.retrieve_saml_uri()

        if uri is not None:
            self.redirect_to(uri)

    def redirect_to(self, uri):
        """Redirect user to a dedicated URI

        Parameters
        ----------
        uri : string
            The URI used to redirect the user after an action

        Raises
        ------
        HTTPSeeOther
            Redirect to the specify URI string parameter
        """

        # Show a link on webpage in case of the redirection is not allowed in
        # web browser
        self.w(a("Redirect to SAML IdP...", href=uri))

        raise HTTPSeeOther(location=uri)

    def retrieve_saml_uri(self):
        """Retrieve the SAML URI if sources has been correctly defined

        Returns
        -------
        str or None
            SAML URI as string if sources are configured, None otherwise
        """

        sources = self._cw.vreg.config.read_sources_file()

        metadata_uri = sources.get("saml", {}).get("saml-metadata-uri", None)
        if metadata_uri is None:
            return None

        request = self._cw._request

        # Add fake login form data to current request to start SAML connection
        # correctly. The SAML Relay State is used to store the postlogin_path
        # URI where the user is redirect after an successful SAML login
        request.GET.update(
            {
                "__login": "saml-login",
                "postlogin_path": request.url,
            }
        )

        return self.get_saml_uri_from_request(request)


class SAMLLogin(LogInTemplate, SAMLLogMixin):
    """Redirect automatically to SAML IdP server

    This class override the default login page to always redirect to IdP server

    See Also
    --------
    cubicweb.web.views.basetemplates.LogInTemplate
    cubicweb_saml.views.SAMLLogMixin
    """

    __select__ = LogInTemplate.__select__ & anonymous_user()
    __regid__ = "login"

    priority = 50

    def call(self):
        """Call the current view

        See Also
        --------
        cubicweb.web.views.basetemplates.LogInOutTemplate.call
        """

        self.on_activate_saml()
        super(SAMLLogin, self).call()


class SAMLLogout(LoggedOutTemplate, SAMLLogMixin):
    """

    See Also
    --------
    cubicweb.web.views.basetemplates.LoggedOutTemplate
    cubicweb_saml.views.SAMLLogMixin
    """

    __select__ = LoggedOutTemplate.__select__ & anonymous_user()
    __regid__ = "loggedout"

    accessible_without_connection = True

    priority = 50

    def call(self):
        """Call the current view

        See Also
        --------
        cubicweb.web.views.basetemplates.LoggedOutTemplate.call
        """

        self.on_activate_saml()
        super(SAMLLogout, self).call()

    def get_saml_uri_from_request(self, request):
        """Retrieve the SAML IdP server URL based on receiving request

        Parameters
        ----------
        request : pyramid.request.Request
            Pyramid request used to retrieve SAML response

        Returns
        -------
        str
            SAML IdP server URL as string

        See Also
        --------
        cubicweb_saml.views.SAMLLogMixin.get_saml_uri_from_request
        """

        saml_uri = super(SAMLLogout, self).get_saml_uri_from_request(request)

        # Use urlparse to only retrieve the beggining of the uri string
        uri = urlparse(saml_uri)

        return "%s://%s" % (uri.scheme, uri.netloc)


def registration_callback(vreg):
    """Add SAML dedicated views inside the CubicWeb registry

    Parameters
    ----------
    vreg : cubicweb.cwvreg.CWRegistryStore
        CubicWeb registry storage instance
    """

    vreg.register_all(globals().values(), __name__)
