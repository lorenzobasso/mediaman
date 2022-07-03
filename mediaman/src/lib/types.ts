export type AxiosParams = { [name: string]: string | number | boolean };

export type Avatar = {
	size: string;
	url: string;
	height: number;
	width: number;
};

export type Channel = {
	id: string;
	title: string;
	description: string;
	customUrl: string;
	published: string;
	country: string;
	uploadPlaylist: string;
	views: number;
	subscribers: number;
	videos: number;
	banner: string;
	following: boolean;
	avatars: Avatar[];
};

export type Chunkable = (string | number | boolean)[];
