export declare enum MessageType {
    GeneralError = 0,
    ParsingDataError = 1,
    ConstraintSolvingError = 2,
    LinkGuideCreatingError = 3,
    InvalidLinksData = 4,
    NoID = 5,
    NoSourceOrTargetID = 6
}
export declare const messageTypes: (string | MessageType)[];
export declare const LinkSourceKeyColumn = "source_id";
export declare const LinkTargetKeyColumn = "target_id";
export declare const isReservedColumnName: (name: string) => boolean;
export declare const KeyColumn = "id";
export declare const ImageKeyColumn = "imageId";
export declare const defaultDelimiter = ",";
export declare const defaultNumberFormat: Readonly<{
    remove: string;
    decimal: string;
}>;
export declare const defaultCurrency: [string, string];
export declare const defaultCurrencySymbol: string;
export declare const defaultDigitsGroup: number[];
export declare const primaryButtonStyles: {
    root: {
        backgroundColor: string;
        color: string;
        borderRadius: number;
        borderColor: string;
        height: number;
    };
    rootHovered: {
        backgroundColor: string;
        color: string;
    };
    rootChecked: {
        backgroundColor: string;
        color: string;
    };
    rootPressed: {
        backgroundColor: string;
        color: string;
    };
};
export declare const fontList: string[];
