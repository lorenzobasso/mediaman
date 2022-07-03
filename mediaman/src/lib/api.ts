import axios from 'axios';
import type { AxiosParams } from './types';

const url = (endpoint: string) => `http://localhost:8000/${endpoint}`;

const get = (endpoint: string, params?: AxiosParams) => axios.get(url(endpoint), { params });
const put = (endpoint: string, params?: AxiosParams) => axios.put(url(endpoint), {}, { params });
const patch = (endpoint: string, params?: AxiosParams) =>
	axios.patch(url(endpoint), {}, { params });

const api = {
	putChannel: (id: string) => put('channel', { id }),
	changeFollow: (id: string) => patch('follow-channel', { id }),
	discoverLibrary: (id: string) => put('library', { id }),
	getFollowed: () => get('channels')
};

export default api;
