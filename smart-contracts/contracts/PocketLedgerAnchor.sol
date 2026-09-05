// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PocketLedgerAnchor
 * @dev Anchors PocketLedger evidence snapshots to the blockchain.
 */
contract PocketLedgerAnchor {
    address public immutable authorizedBackend;

    struct StateAnchor {
        bytes32 dataHash;
        uint256 timestamp;
    }

    // Mapping from merchantID string to their latest anchored state
    mapping(string => StateAnchor) private merchantStates;

    event StateAnchored(string indexed merchantID, bytes32 dataHash, uint256 timestamp);

    error Unauthorized();
    error InvalidHash();
    error EmptyMerchantID();

    modifier onlyBackend() {
        if (msg.sender != authorizedBackend) {
            revert Unauthorized();
        }
        _;
    }

    constructor() {
        authorizedBackend = msg.sender;
    }

    /**
     * @notice Logs a new state anchor for a merchant.
     * @param merchantID The unique identifier for the merchant.
     * @param dataHash The SHA256 hash of (merchant_id + health_score + cumulative_revenue).
     */
    function logIdentityState(string calldata merchantID, bytes32 dataHash) external onlyBackend {
        if (bytes(merchantID).length == 0) {
            revert EmptyMerchantID();
        }
        if (dataHash == bytes32(0)) {
            revert InvalidHash();
        }

        merchantStates[merchantID] = StateAnchor({
            dataHash: dataHash,
            timestamp: block.timestamp
        });

        emit StateAnchored(merchantID, dataHash, block.timestamp);
    }

    /**
     * @notice Retrieves the latest anchored state for a merchant.
     * @param merchantID The unique identifier for the merchant.
     * @return dataHash The most recently anchored data hash.
     * @return timestamp The block timestamp when the state was anchored.
     */
    function getLatestState(string calldata merchantID) external view returns (bytes32, uint256) {
        StateAnchor memory anchor = merchantStates[merchantID];
        return (anchor.dataHash, anchor.timestamp);
    }
}
