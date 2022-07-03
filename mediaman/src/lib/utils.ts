import type { Chunkable } from './types';

export const range = (n: number, start?: number, step?: number) =>
	Array(n)
		.fill(0)
		.map((_, i) => i * (step ?? 1) + (start ?? 0));

export const _chunk = (array: Chunkable, size: number) =>
	range(Math.ceil(array.length / size), 0, size).map((begin) => array.slice(begin, begin + size));

export const _chunk_rev = (array: Chunkable, size: number) =>
	_chunk(array.reverse(), size)
		.map((c) => c.reverse())
		.reverse();

export const chunk = (array: Chunkable, size: number, reverse = false) =>
	reverse ? _chunk_rev(array, size) : _chunk(array, size);

export const prettyNum = (n: number) =>
	chunk(String(n).split(''), 3)
		.map((n) => n.join(''))
		.join(',');
