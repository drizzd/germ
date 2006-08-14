#
#  txt/errmsg.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

error_lvl = [
	{	'en': 'Debug' },
	{	'en': 'Info' },
	{	'en': 'Notice',
		'de': 'Merke' },
	{	'en': 'Warning',
		'de': 'Achtung' },
	{	'en': 'Error',
		'de': 'Fehler' },
	{	'en': 'Failure',
		'de': 'Fehler' } ]

#"The system dministrator has been informed and the problem will be dealt with as soon as possible."
failure = """
<P>
This should not happen. We are sorry for the inconvenience.<BR />
<BR />
If your time permits you could describe what happened to help solve the
problem.<BR />
</P>
"""

unimplemented = {
	'en': 'Not implemented',
	'de': 'Nicht implementiert' }

abstract_func = {
	'en': 'Invocation of an abstract function',
	'de': 'Aufruf einer abstrakten Funktion' }

abstract_inst = {
	'en': 'Instantiation of abstract class',
	'de': 'Instanziierung einer abstrakten Klasse' }

tried_locking_unset_attr = {
	'en': 'Attempt to lock unset attribute',
	'de': 'Versuch ein nicht gesetztes Attribut zu sperren' }

permission_denied = {
	'en': 'Permission denied',
	'de': 'Zugriff verweigert' }

no_valid_keys = {
	'en': 'No valid keys available',
	'de': 'Kein Schl"ussel verf"ugbar' }

invalid_key = {
	'en': 'Invalid key (not available)',
	'de': 'Ung"ultiger Schl"ussel (nicht verf"ugbar)' }

invalid_parm = {
	'en': 'Invalid parameter',
	'de': 'Ung"ultiger Parameter' }

missing_parm = {
	'en': 'Missing parameter',
	'de': 'Parameter fehlt' }

missing_pk_lock = {
	'en': 'Please choose an entry',
	'de': 'Bitte w"ahlen Sie einen Eintrag' }

missing_lock = {
	'en': 'There is at least one parameter that needs to be locked',
	'de': 'Mindestens ein Parameter muss festgelegt werden' }

do_not_exec = {
	'en': 'Please confirm',
	'de': 'Bitte best"atigen Sie' }

nonexistent_attr = {
	'en': 'Nonexistent attribute',
	'de': 'Attribut existiert nicht' }

attr_choice_nooptions = {
	'en': 'Choice attribute needs at least one option',
	'de': 'Das choice Attribut ben"otigt mindestens eine Option' }

unknown_db_type = {
	'en': 'Unkown database type' }

invalid_name = {
	'en':	"Invalid name (allowed characters: 'a-z', '0-9', '_', ' '; do " \
			"not start with a space)",
	'de':	"Ung\"ultiger Name (erlaubte Zeichen: 'a-z', '0-9', '_', ' '; " \
			"nicht mit einem Leerzeichen beginnen)" }

invalid_identifier = {
	'en':	"Invalid identifier (allowed characters: 'a-z', '0-9', '_'; do " \
			"not start with a number)",
	'de':	"Ung\"ultige Bezeichnung (erlaubte Zeichen: 'a-z', '0-9', '_'; " \
			"nicht mit einer Zahl beginnen)" }

attr_error = {
	'en': 'The following attributes caused errors',
	'de': 'Die folgenden Attribute verursachen Fehler' }
