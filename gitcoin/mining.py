from datetime import datetime
from threading import Thread
from logic import State, rebase_on_remotes
from hashing_utils import mine_block

def mine(state: State):
    """Mines a block while pulling from remotes.
    """
    last_rebase_time = datetime.now()

    while True:
        if mine_block.mine(0x10000):
            break

        if (last_rebase_time - datetime.now()).total_seconds() > 10:
            last_rebase_time = datetime.now()
            thread = Thread(target=rebase_on_remotes, args=state)
            thread.start()
    state.repo.git.push()

