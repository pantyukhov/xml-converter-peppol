import xml.etree.ElementTree as ET


def add_elementtree_as_child(parent, child):
    """
    Add an elementtree as a child of another elementtree.
    :param parent: The parent elementtree.
    :param child: The child elementtree.
    :return:
    """
    parent.append(child)


def remove_elementtree_as_child_by_tag(parent, tag):
    """
    Remove an elementtree as a child of another elementtree.
    :param parent: The parent elementtree.
    :param tag: The tag of the child elementtree.
    :return:
    """
    for child in parent:
        if child.tag == tag:
            parent.remove(child)
            break


def create_invoice_elementtree(invoice, kbo_number):
    """
    Create an elementtree from an invoice xml.
    :param invoice: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Add all children with ns1 prefix to invoice.
    invoice = add_ns1_children(invoice)
    invoice = convert_supplier_party(invoice, kbo_number)
    invoice = convert_customer_party(invoice, kbo_number)
    invoice = convert_payment_means(invoice)
    invoice = convert_tax_total(invoice)
    invoice = convert_invoice_line(invoice)
    return invoice


def add_ns1_children(invoice):
    """
    Add all children with ns1 prefix to invoice.
    :param invoice: The invoice xml in elementtree.
    :return: the elementtree.
    """
    add_customization_id(invoice)
    add_profile_id(invoice)
    change_invoice_type_code(invoice)
    change_document_currency_code(invoice)
    convert_tax_total(invoice)
    return invoice


def convert_supplier_party(invoice, kbo_number):
    """
    Convert the supplier party to a new party.
    :param invoice: The invoice xml in elementtree.
    :return:
    """
    # Get the supplier party.
    supplier_party = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty')
    # Find party child.
    party = find_party(supplier_party)
    party = add_endpoint_id(party, kbo_number)
    party = remove_website_uri(party)
    party = change_identification_code_list_id(party)
    party = remove_scheme_id_of_id(party)
    party = change_party_legal_entity(party)
    party = electronic_mail_add_languageId(party)
    return invoice


def convert_customer_party(invoice, kbo_number):
    """
    Convert the customer party to a new party.
    :param invoice: The invoice xml in elementtree.
    :param kbo_number: The kbo number of the customer.
    :return: The elementtree.
    """
    # Get the customer party.
    customer_party = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty')
    # Find party child.
    party = find_party(customer_party)
    party = add_endpoint_id(party, kbo_number)
    party = change_identification_code_list_id(party)
    party = remove_scheme_id_of_id(party)
    party = add_party_legal_entity(party, kbo_number)
    party = electronic_mail_add_languageId(party)
    return invoice


def convert_payment_means(invoice):
    """
    Convert the payment means to a new payment means.
    :param invoice:
    :return:
    """
    payment_means = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PaymentMeans')
    # Find payment means code child.
    payment_means_code = payment_means.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentMeansCode')
    # Change listid of payment means code.
    payment_means_code.set('listID', 'UNCL4461')
    # Find payeefinancialaccount child.
    payeefinancialaccount = payment_means.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PayeeFinancialAccount')
    # Find id child.
    id = payeefinancialaccount.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Change schemename to schemeid.
    id.attrib.pop('schemeName')
    id.set('schemeID', 'IBAN')
    # Find financialinstitutionbranch child.
    financialinstitutionbranch = payeefinancialaccount.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}FinancialInstitutionBranch')
    # Find financialinstitution child.
    financialinstitution = financialinstitutionbranch.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}FinancialInstitution')
    # Find id child.
    id = financialinstitution.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Change schemename to schemeid.
    id.attrib.pop('schemeName')
    id.set('schemeID', 'BIC')
    # Return the invoice.
    return invoice


def convert_tax_total(invoice):
    """
    Convert the tax total to a new tax total.
    :param invoice:
    :return:
    """
    tax_total = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal')
    # Find tax subtotal child.
    tax_subtotal = tax_total.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxSubtotal')
    # Remove percent child from tax_subtotal.
    for child in tax_subtotal:
        if child.tag == '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Percent':
            tax_subtotal.remove(child)
    # Find tax category child.
    tax_category = tax_subtotal.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxCategory')
    # Find id child.
    id = tax_category.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Remove all attributes from id.
    id.attrib.clear()
    # Add schemeid to id.
    id.set('schemeID', 'UNCL5305')
    id.text = 'S'
    # Find tax scheme child.
    tax_scheme = tax_category.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
    # Find id child.
    id = tax_scheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Remove all attributes from id.
    id.attrib.clear()
    return invoice


def convert_invoice_line(invoice):
    """
    Convert the invoice line to a new invoice line.
    :param invoice:
    :return:
    """
    # Find invoice line.
    invoice_line = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoiceLine')
    # Find item child.
    item = invoice_line.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Item')
    # Remove item child.
    invoice_line.remove(item)
    # Find invoiced quantity child.
    invoiced_quantity = invoice_line.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoicedQuantity')
    # Add unitCode="C62" unitCodeListID="UNECERec20" to invoiced_quantity.
    invoiced_quantity.set('unitCode', 'C62')
    invoiced_quantity.set('unitCodeListID', 'UNECERec20')
    # Find tax total child.
    tax_total = invoice_line.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal')
    # Find tax subtotal child.
    tax_subtotal = tax_total.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxSubtotal')
    # Find tax category child.
    tax_category = tax_subtotal.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxCategory')
    # Find id child.
    id = tax_category.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Remove all attributes from id.
    id.attrib.clear()
    # Add schemeid to id.
    id.set('schemeID', 'UNCL5305')
    id.text = 'S'
    # Find tax scheme child.
    tax_scheme = tax_category.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
    # Find id child.
    id = tax_scheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
    # Remove all attributes from id.
    id.attrib.clear()
    # Create new item element.
    item = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Item')
    # Add it to invoice line as 3th child.
    invoice_line.insert(3, item)
    ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name').text = 'Classified taxcategory'
    # Create new classified tax category child.
    classified_tax_category = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}ClassifiedTaxCategory')
    # Add all childs from tax_category to item.
    for child in tax_category.getchildren():
        classified_tax_category.append(child)
    # Remove Tax total child.
    invoice_line.remove(tax_total)
    # Find price child.
    price = invoice_line.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Price')
    # Find and remove base quantity child.
    base_quantity = price.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}BaseQuantity')
    return invoice


def add_customization_id(invoice):
    """
    Add an elementtree with tag 'CustomizationID' and text 'urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0' as a child of invoice.
    :param invoice: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Add elementtree with tag 'CustomizationID' and text 'urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0' as a child of invoice.
    element = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID')
    element.text = 'urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0'
    # Add element as second child of invoice.
    invoice.insert(1, element)
    return invoice


def add_profile_id(invoice):
    """
    Add an elementtree with tag 'ProfileID' and text 'urn:fdc:peppol.eu:2017:poacc:billing:01:1.0' as a child of invoice.
    :param invoice: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Add elementtree with tag 'ProfileID' and text 'urn:fdc:peppol.eu:2017:poacc:billing:01:1.0' as a child of invoice.
    element = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ProfileID')
    element.text = 'urn:fdc:peppol.eu:2017:poacc:billing:01:1.0'
    # Add element as third child of invoice.
    invoice.insert(2, element)
    return invoice


def change_invoice_type_code(invoice):
    """
    Add listid to invoicetypecode.
    :param invoice:
    :return:
    """
    # Add listid to invoicetypecode.
    for child in invoice:
        if child.tag == '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoiceTypeCode':
            child.set('listID',"UNCL1001")
            break
    return invoice


def change_document_currency_code(invoice):
    """
    Add listid to documentcurrencycode.
    :param invoice: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Add listid to documentcurrencycode.
    for child in invoice:
        if child.tag == '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DocumentCurrencyCode':
            child.set('listID', "ISO4217")
            print('here')
            break
    return invoice


def find_party(invoice):
    """
    Find the party in the invoice.
    :param invoice: The invoice xml in elementtree.
    :return: The party in the invoice.
    """
    # Find the party in the invoice.
    party = invoice.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party')
    return party


def add_endpoint_id(xml, kbo_number):
    """
    Add an elementtree with tag 'EndpointID' and text kbo_number as a child of invoice.
    :param xml: The invoice xml in elementtree.
    :param kbo_number: The kbo_number.
    :return: The elementtree.
    """
    # Add elementtree with tag 'EndpointID' and text kbo_number as a child of invoice.
    element = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndpointID')
    element.text = kbo_number
    element.set('schemeID', '0208')
    # Add element as first child of party.
    xml.insert(0, element)
    return xml


def change_identification_code_list_id(xml):
    """
    Add listid to identificationcode.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find child with tag postaladdress.
    postallAdress = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PostalAddress')
    # Print children of postaladdress.
    print('##############################')
    for child in postallAdress:
        print(child.tag)
    # Find child with tag identificationcode and change listid.
    identification_code = postallAdress.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
    if identification_code is not None:
        identification_code.set('listID', "ISO3166-1:Alpha2")
    return xml


def remove_scheme_id_of_id(xml):
    """
    Remove schemeid from id.
    :param xml:
    :return:
    """
    # Find child with tag partytaxscheme.
    partytaxscheme = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme')
    if(partytaxscheme is not None):
        # Find child with tag taxscheme and remove schemeid.
        taxscheme = partytaxscheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
        # Find child with tag id and remove schemeid.
        id = taxscheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        id.attrib.pop('schemeID')
        id.attrib.pop('schemeAgencyID')
    return xml


def electronic_mail_add_languageId(xml):
    """
    Add languageId to electronicmail.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find child with tag contact.
    contact = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Contact')
    # Find child with tag electronicmail and add languageId.
    electronic_mail = contact.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ElectronicMail')
    electronic_mail.set('languageID', "NL")
    return xml


def remove_website_uri(xml):
    """
    Remove website uri from party.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find child with tag WebsiteURI.
    for child in xml:
        if child.tag == '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}WebsiteURI':
            xml.remove(child)
    return xml


def change_party_legal_entity(xml):
    """
    Change party legal entity.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find child with tag partylegalentity.
    partylegalentity = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')
    # Find child with tag country
    country = partylegalentity.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country')
    # Find identificationcode and change listid.
    identification_code = country.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
    identification_code.set('listID', "ISO3166-1:Alpha2")
    return xml


def add_party_legal_entity(xml, endpointId):
    """
    Add party legal entity.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find partytaxscheme.
    partytaxscheme = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme')
    if(partytaxscheme is not None):
        # Find child with tag registrationname.
        registrationname = partytaxscheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
        # Find child with tag companyid.
        companyid = partytaxscheme.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
        # Make new partylegalentity.
        partylegalentity = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')
        # Add registrationname and companyid as childs.
        partylegalentity.append(registrationname)
        partylegalentity.append(companyid)
        # Add partylegalentity as child to party.
        partytaxscheme.append(xml)
    else:
        xml = add_party_legal_entity_with_endpointid(xml, endpointId)
    return xml


def add_party_legal_entity_with_endpointid(xml, endpointId):
    """
    Add party legal entity.
    :param xml: The invoice xml in elementtree.
    :return: The elementtree.
    """
    # Find partyname.
    partyname = xml.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
    # Find child with tag name.
    name = partyname.find('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
    # Create new partylegalentity.
    partylegalentity = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')
    # Create new registrationname.
    registrationname = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
    # Create new companyid.
    companyid = ET.Element('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
    # Set registrationname and companyid.
    registrationname.text = name.text
    companyid.text = endpointId
    # Add registrationname and companyid as childs.
    partylegalentity.append(registrationname)
    partylegalentity.append(companyid)
    # Add partylegalentity as one to last child to party.
    xml.insert(len(xml.getchildren())-1, partylegalentity)
    return xml
