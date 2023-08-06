export declare function useLocalStorage<Type extends string | number | boolean | Record<string, unknown>>(initialValue: Type, storageKey: string): [Type, (newValue: Type) => void];
