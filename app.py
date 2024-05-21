import streamlit as st
import json
from datetime import datetime
from background import background_image
from code_map import code_map
from hints import hint_map, author_hint_link, final_stm, start_stm
from title import site_title

st.set_page_config(page_title='Escape Room', page_icon='🔓', layout="wide")
st.title('Escape from the Library')

teams = st.session_state.get('teams', {})
with open('teams.json', 'r') as f:
    teams = json.load(f)

background_image()
site_title()

team_logged_in = st.session_state.get('team_logged_in', False)
team_name = st.session_state.get('team_name', '')


if not team_logged_in:
    team_name = st.selectbox('Select your team', [''] + list(teams.keys()))

    if team_name == '':
        team_name = st.text_input('Enter your team name')
        players = 6
        player_names = []
        col1, col2 = st.columns(2)
        count = 0
        for i in range(players):
            if count % 2 == 0:
                player_names.append(col1.text_input(f'Enter player {i+1} name'))
            else:
                player_names.append(col2.text_input(f'Enter player {i+1} name'))
            count += 1
        if team_name:
            st.write('Note: When you click the Start button, you will start the game and you will not be able to change your team name or player names. Additionally, your time will start counting.')
            if st.button('Login'):
                teams[team_name] = {
                    'players': player_names,
                    'time_started': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                with open('teams.json', 'w') as f:
                    json.dump(teams, f)
                st.session_state.teams = teams
                st.session_state.team_logged_in = True
                st.session_state.team_name = team_name
                st.session_state.player_names = player_names
                st.rerun()
    else:
        st.session_state.team_logged_in = True
        st.session_state.team_name = team_name
        st.session_state.player_names = teams[team_name]['players']
        st.session_state.hints_requested = teams[team_name].get('hints_requested', [0])
        st.session_state.ready_to_start = True
        st.rerun()

team_logged_in = st.session_state.get('team_logged_in', False)
team_name = st.session_state.get('team_name', '')
welcome_message = st.session_state.get('welcome_message', True)
ready_to_start = st.session_state.get('ready_to_start', False)
hints_requested = st.session_state.get('hints_requested', [0])
author_hint = st.session_state.get('author_hint', '')
author_hints = st.session_state.get('author_hints', [])
hint_by_author = st.session_state.get('hint_by_author', None)
new_click = st.session_state.get('new_click', False)
it_code = st.session_state.get('it_code', False)

if team_logged_in:
    if welcome_message:
        if 'started' not in teams[team_name].keys():
            st.write(f'Welcome Team {team_name}!')
            st.write(start_stm)
        
            if st.button('Ready to start'):
                teams[team_name]['started'] = True
                with open('teams.json', 'w') as f:
                    json.dump(teams, f)
                st.session_state.welcome_message = False
                st.session_state.ready_to_start = True
                st.rerun()
        else:
            st.session_state.welcome_message = False
            st.session_state.ready_to_start = True
            st.rerun()

if ready_to_start:
    code_entered = st.session_state.get('code_entered', False)
    code = str(st.text_input('Enter a code you found in the room', value='')).strip()
    if code:
        if st.button('Submit'):
            st.session_state.code_entered = True
            st.session_state.code = code
            st.rerun()
    
    code_entered = st.session_state.get('code_entered', False)
    code = st.session_state.get('code', '')
    code_entered = str(code_entered) if code_entered else code_entered
    if code in code_map.keys():
        if code == list(code_map.keys())[0]:
            st.write(f'Congratulations Team {team_name}! You have escaped the library!')
            st.write(f'You have requested {len(hints_requested)-1 + len(list(set(author_hints)))} hints.')
            time_started = datetime.strptime(teams[team_name]['time_started'], '%Y-%m-%d %H:%M:%S')
            time_ended = datetime.now()
            time_elapsed = time_ended - time_started
            st.write(f'You have completed the game in {time_elapsed}')
            teams[team_name]['time_ended'] = time_ended.strftime('%Y-%m-%d %H:%M:%S')
            teams[team_name]['time_elapsed'] = str(time_elapsed)
            teams[team_name]['hints_requested'] = hints_requested
            with open('teams.json', 'w') as f:
                json.dump(teams, f)
            st.session_state.teams = teams
        elif code == '1986':
            st.write(code_map[code])
            it_code = True
            st.session_state.it_code = it_code
        else:
            st.write(code_map[code])

    elif code not in code_map.keys() and code_entered:
        st.write('Sorry, wrong code! Try again!')

    with st.expander('Need help?'):
        st.write('If you need help, you can ask the librarian for a hint!')
        st.write('If you know the last name of the author of the book, you can ask the librarian for a specific hint!')
        author_hint = st.text_input('Enter the last name of the author of the book', author_hint).lower()
        show_hint = True
        if st.button('Ask the librarian for a hint'):
            new_click = True
            st.session_state.new_click = new_click
            hint_by_author = None
            if author_hint in author_hint_link:
                hint_by_author = author_hint_link[author_hint]
                author_hints.append(author_hint)
                st.session_state.author_hints = author_hints
                st.session_state.hint_by_author = hint_by_author
                teams[team_name]['author_hints'] = author_hints
                with open('teams.json', 'w') as f:
                    json.dump(teams, f)
            elif author_hint != '':
                st.write('Sorry, I do not have a hint for that author.')

            if hints_requested >= len(hint_map.keys()) + len(list(set(author_hints))) - 1:
                st.write('You have already requested the maximum number of hints.')
                show_hint = False
            else:
                hint_to_add = max(hints_requested) + 1
                while hint_to_add in author_hints:
                    hint_to_add += 1
                hints_requested.append(hint_to_add)
                st.session_state.hints_requested = hints_requested
                teams[team_name]['hints_requested'] = hints_requested
                with open('teams.json', 'w') as f:
                    json.dump(teams, f)
                st.rerun()

        if hints_requested > 1 and show_hint:
            new_click = st.session_state.get('new_click', False)
            st.title('Hints')
            st.write(f'You have requested {hints_requested + len(list(set(author_hints)))} hint(s).')

            if hint_by_author:
                st.write(f"- {hint_map[hint_by_author]}")
                st.session_state.hint_by_author = None
                hint_by_author = None
                st.session_state.author_hint = ''
            elif new_click:
                display_hint = hints_requested
                st.write(f"- {hint_map[display_hint]}")
            new_click = False
            
    
    if st.button('Check Time'):
        time_started = datetime.strptime(teams[team_name]['time_started'], '%Y-%m-%d %H:%M:%S')
        time_ended = datetime.now()
        time_elapsed = time_ended - time_started
        time_elapsed = str(time_elapsed).split('.')[0]
        st.write(f'You have been playing for {time_elapsed}')

    if it_code:
        if st.button('Ready for Final Challenge'):
            st.write(final_stm)
            teams[team_name]['final_challenge'] = True
            teams[team_name]['final_challenge_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('teams.json', 'w') as f:
                json.dump(teams, f)
        