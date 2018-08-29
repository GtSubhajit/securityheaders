from securityheaders.checkers import SyntaxChecker, FindingType, Finding, FindingSeverity
from securityheaders.models import ModelFactory

class UnknownDirectiveChecker(SyntaxChecker):

    def check(self, headers, opt_options=dict()):
        headernames = ModelFactory().getheadernames()

        findings = []
        for header in headernames:
            hdr = ModelFactory().getheader(header)
            try:
                obj = self.extractheader(headers, hdr)
                if obj and obj.parsedstring:
                    findings.extend(self.mycheck(obj))
            except:
                pass
        return findings

    def mycheck(self, data):
        findings = []

        if not data:
            return findings

        directiveclazz = data.directive
        seperator = directiveclazz.directivevalueseperator()
        for directive in data.keys():
            if not directiveclazz.isDirective(directive):
                if directive.endswith(seperator):
                    findings.append(Finding(data.headerkey, FindingType.UNKNOWN_DIRECTIVE,str(data.headerkey) + " directives don't end with a " + str(seperator),FindingSeverity.SYNTAX, None, directive))
                else:
                    findings.append(Finding(data.headerkey, FindingType.UNKNOWN_DIRECTIVE,'Directive "' + str(directive) + '" is not a known ' + str(data.headerkey) + ' directive.',FindingSeverity.SYNTAX,None, directive))

        return findings