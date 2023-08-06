from pdb import set_trace as T
import numpy as np

from collections.abc import MutableMapping

import gym


def pad_const_num_agents(dummy_ob, pad_to, obs, rewards, dones, infos):
    '''Requires constant integer agent keys'''
    for i in range(pad_to):
        if i not in obs:                                                  
            obs[i]     = dummy_ob                                         
            rewards[i] = 0                                                 
            infos[i]   = {}
            dones[i]   = False

def const_horizon(dones):
    for agent in dones:
        dones[agent] = True

    return dones

def pack_atn_space(atn_space):
    flat = flatten(atn_space)

    lens = []
    for e in flat.values()
        lens.append(e.shape)
    
    return gym.spaces.MultiDiscrete(lens) 

def pack_obs_space(obs_space, dtype=np.float32):
    flat = flatten(obs_space)

    n = 0
    for e in flat.values():
        n += np.prod(e.shape)

    return gym.spaces.Box(
        low=-2**20, high=2**20,
        shape=(int(n),), dtype=dtype
    )

def flatten(nested_dict, parent_key=[]):
    items = []
    for k, v in nested_dict.items():
        new_key = parent_key [k]
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_ob(ob):
    flat = flatten(obs)
    vals = list(flat.values())
    return np.concatenate(vals)

def pack_obs(obs):
    return {k: flatten_ob(v) for k, v in obs.items()}

def pack_and_batch_obs(obs):
    obs = list(pack_obs(obs))
    return np.stack(obs, axis=0)

def unpack_obs(obs_space, packed_obs):
    batch = packed_obs.shape[0]
    obs = {}
    idx = 0

    for key_list, val in flatten(obs).items():
        obs_ptr = obs
        for key in key_list:
            if key not in obs_ptr:
                obs_ptr[key] = {}

        inc = np.prod(val.shape)
        obs_ptr[key] = packed_obs[:, idx:idx + inc].reshape(batch, *val.shape)

    return obs