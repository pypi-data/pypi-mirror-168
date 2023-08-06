export declare class HistoryManager<StateType> {
    statesBefore: StateType[];
    statesAfter: StateType[];
    addState(state: StateType): void;
    undo(currentState: StateType): StateType;
    redo(currentState: StateType): StateType;
    clear(): void;
    getState(): {
        statesAfter: StateType[];
        statesBefore: StateType[];
    };
    setState(statesAfter: StateType[], statesBefore: StateType[]): void;
}
