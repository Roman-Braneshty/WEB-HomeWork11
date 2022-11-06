import sqlalchemy.exc
from flask import render_template, request, flash, redirect, url_for, session, make_response
import pathlib
from . import app
from src.queries import contact, emails, addresses, phones, user, notes


@app.route('/healthcheck', strict_slashes=False)
def healthcheck():
    return 'I am worhing'


@app.route('/start', strict_slashes=False)
def start_page():
    # auth = True if 'username' in session else False
    nick = user.get_user(session['user_id']['id']).nick
    contacts = contact.get_all_contacts(session['user_id']['id'])
    contact_notes = notes.get_all_notes(session['user_id']['id'])
    return render_template('user.html', nick=nick, contacts=contacts, contact_notes=contact_notes)


@app.route('/', strict_slashes=False)
def index():
    # auth = True if 'username' in session else False
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    # auth = True if 'username' in session else False
    if request.method == 'POST':
        if request.form.get('login'):
            return redirect(url_for('login'))

        nick = request.form.get('nickname')
        password = request.form.get('password')
        print(nick, password, user.find_by_nick(nick))
        if user.find_by_nick(nick) is None:
            registration_contact = user.update_login_for_user(nick, password)
            return render_template('login.html')
        else:
            flash('User already exist')
            return render_template('registration.html', message='User already exist')

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    # auth = True if 'username' in session else False
    if request.method == 'POST':
        nick = request.form.get('nickname')
        password = request.form.get('password')
        login_data = user.checkout_login_for_user(nick, password)
        if login_data is None:
            flash('pass')
            return redirect(url_for('login'))

        session['user_id'] = {'id': login_data.id}
        response = make_response(redirect(url_for('start_page')))
        return response
    return render_template('login.html')


@app.route('/logout', strict_slashes=False)
def logout():
    session.pop('user_id')
    response = make_response(redirect(url_for('login')))

    return response


@app.route('/page/<contact_id>', strict_slashes=False)
def contact_page(contact_id):
    # auth = True if 'username' in session else False
    contact_first_name = contact.get_contact(session['user_id']['id'], contact_id).first_name
    contact_last_name = contact.get_contact(session['user_id']['id'], contact_id).last_name
    contact_birthday = contact.get_contact(session['user_id']['id'], contact_id).birthday
    contact_addresses = [address.address for address in addresses.get_contact_address(contact_id)]
    contact_phones = [phone.phone for phone in phones.get_contact_phone(contact_id)]
    contact_emails = [email.email for email in emails.get_contact_emails(contact_id)]

    return render_template('index.html',
                           contact_id=contact_id,
                           birthday=contact_birthday,
                           addresses=contact_addresses,
                           phones=contact_phones,
                           emails=contact_emails,
                           first_name=contact_first_name,
                           last_name=contact_last_name)


@app.route('/add_info', methods=['GET', 'POST'], strict_slashes=False)
def add_info():
    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')

        contact.upload_contact_for_user(session['user_id']['id'],
                                        first_name=first_name,
                                        last_name=last_name,
                                        birthday=birthday)

        contact_id = contact.get_contact_id(session['user_id']['id'],
                                            first_name=first_name,
                                            last_name=last_name,
                                            birthday=birthday)
        print(contact_id)

        contact_email = request.form.get('email')
        if contact_email != "":
            try:
                emails.upload_email_for_user(contact_id, contact_email)
            except sqlalchemy.exc.IntegrityError:
                flash('This email already added')

        contact_address = request.form.get('address')
        if contact_address != "":
            addresses.upload_address_for_user(contact_id, contact_address)

        contact_phone = request.form.get('phone')
        if contact_phone != "":
            phones.upload_phone_for_user(contact_id, contact_phone)

        response = make_response(redirect(url_for('start_page')))
        return response
    return render_template('add_info.html')


@app.route("/delete_contact/<contact_id>", strict_slashes=False)
def delete_contact(contact_id):
    contact.delete_contact(session['user_id']['id'], contact_id)
    return redirect("/start")


@app.route('/edit_info/<contact_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_info(contact_id):
    if request.method == 'POST':
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        birthday = request.form.get('birthday').strip()
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')

        if first_name != '':
            contact_first_name = contact.update_first_name(session['user_id']['id'], contact_id, first_name)
        if last_name != '':
            contact_last_name = contact.update_last_name(session['user_id']['id'], contact_id, last_name)
        if birthday != '':
            contact_birthday = contact.update_birthday(session['user_id']['id'], contact_id, birthday)
        if email != '':
            contact_email = emails.upload_email_for_user(contact_id, email)
        if address != '':
            contact_address = addresses.upload_address_for_user(contact_id, address)
        if phone != '':
            contact_address = phones.upload_phone_for_user(contact_id, phone)

        return redirect(url_for('start_page'))

    return render_template('add_info.html', edit=True, contact_id=contact_id)


@app.route('/delete_info/<contact_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_info(contact_id):
    if request.method == 'POST':
        if request.form.get('value') == 'address' or \
                request.form.get('value') == 'phone' or \
                request.form.get('value') == 'email':
            radio = request.form.get('value')
            values = []
            if radio == 'address':
                values = [address for address in addresses.get_contact_address(contact_id)]
            if radio == 'phone':
                values = [phone for phone in phones.get_contact_phone(contact_id)]
            if radio == 'email':
                values = [email for email in emails.get_contact_emails(contact_id)]
            return render_template('remove.html', radio=radio, values=values, contact_id=contact_id)
        else:
            del_element = request.form.get('value_select')

            del_element_pieces = del_element.replace('<', '').replace('>', '').split(' ')

            if del_element_pieces[0] == 'Email':
                emails.delete_email(contact_id, del_element_pieces[1])
            if del_element_pieces[0] == 'Address':
                addresses.delete_address(contact_id, del_element_pieces[1])
            if del_element_pieces[0] == 'Phone':
                phones.delete_phone(contact_id, del_element_pieces[1])

            return render_template('remove.html', contact_id=contact_id)

    return render_template('remove.html', contact_id=contact_id)


@app.route('/note', methods=['GET', 'POST'], strict_slashes=False)
def note():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        tags = request.form.getlist("tags")
        tags_obj = []
        for tag in tags:
            tags_obj.append(notes.get_tag(tag))
        user_note = notes.add_note(name, description, tags_obj, session['user_id']['id'])
        return redirect("/note")
    else:
        tags = notes.get_all_tags()
    return render_template('note.html', tags=tags)


@app.route('/tag', methods=['GET', 'POST'], strict_slashes=False)
def tag():
    if request.method == "POST":
        name = request.form.get("name")
        notes.update_tag(name)
        return render_template('tag.html')
    return render_template('tag.html')


@app.route('/note_detail/<note_id>', methods=['GET', 'POST'], strict_slashes=False)
def note_detail(note_id):
    note = notes.get_note(session['user_id']['id'], note_id)
    return render_template('note_detail.html', note=note)


