#!/bin/bash
if [ -f "/data/NEW_INSTALL" ]; then
    echo "Configuring Drone..."

    # Create the admin user
    sqlite3 /data/database.sqlite "INSERT INTO users (user_login, user_email, user_admin, user_machine, user_active, user_syncing, user_synced, user_created, user_updated, user_last_login, user_avatar, user_oauth_expiry, user_hash, user_oauth_token, user_oauth_refresh) VALUES ('gitadmin', 'gitadmin@${EMAIL_DOMAIN:-domain.local}', 1, 0, 1, 0, 0, $(date +%s), $(date +%s), $(date +%s), '', 0, '$(echo gitadmin|md5sum|cut -d ' ' -f 1|base64)', '', '');"

    # Create users from the /config/users.csv file
    if [ -f "/config/users.csv" ]; then
        i=1
        echo "Creating users from /config/users.csv"
        while IFS="," read -r username email password || [ -n "$username" ]; do
            # Validate that username, email and password are not empty
            if [ -z "$username" ] || [ -z "$email" ] || [ -z "$password" ]; then
                echo "Invalid user: $username"
                continue
            fi
            echo "Creating user: $username"
            
            PEM=$( cat /tmp/private.pem )
            FINGERPRINT=$( openssl rsa -in <(echo -n "${PEM}") -pubout -outform DER 2>/dev/null | openssl dgst -sha256 -binary | openssl enc -base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )
            NOW=$( date +%s )
            IAT="${NOW}"
            EXP=$((NOW+36000))
            HEADER_RAW='{"alg": "RS256","kid": "'"$FINGERPRINT"'","typ": "JWT"}'
            HEADER=$( echo -n "${HEADER_RAW}" | openssl base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )#

            PAYLOAD_RAW_AUTH='{"iat":'"${IAT}"',"exp":'"${EXP}"',"gnt":'"${i}"', "tt":0}'
            PAYLOAD_AUTH=$( echo -n "${PAYLOAD_RAW_AUTH}" | openssl base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )
            HEADER_PAYLOAD_AUTH="${HEADER}"."${PAYLOAD_AUTH}"
            SIGNATURE_AUTH=$( openssl dgst -sha256 -sign <(echo -n "${PEM}") <(echo -n "${HEADER_PAYLOAD_AUTH}") | openssl base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )
            JWT_AUTH="${HEADER_PAYLOAD_AUTH}"."${SIGNATURE_AUTH}"

            PAYLOAD_RAW_REFRESH='{"iat":'"${IAT}"',"exp":'"${EXP}"',"gnt":'"${i}"', "tt":1}'
            PAYLOAD_REFRESH=$( echo -n "${PAYLOAD_RAW_REFRESH}" | openssl base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )
            HEADER_PAYLOAD_REFRESH="${HEADER}"."${PAYLOAD_REFRESH}"
            SIGNATURE_REFRESH=$( openssl dgst -sha256 -sign <(echo -n "${PEM}") <(echo -n "${HEADER_PAYLOAD_REFRESH}") | openssl base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n' )
            JWT_REFRESH="${HEADER_PAYLOAD_REFRESH}"."${SIGNATURE_REFRESH}"

            echo $JWT_AUTH
            echo $JWT_REFRESH

            sqlite3 /data/database.sqlite "INSERT INTO users (user_login, user_email, user_admin, user_machine, user_active, user_syncing, user_synced, user_created, user_updated, user_last_login, user_avatar, user_oauth_expiry, user_hash, user_oauth_token, user_oauth_refresh) VALUES ('$username', '$email', 0, 0, 1, 0, 0, $(date +%s), $(date +%s), $(date +%s), '', $EXP, '$(echo $username|md5sum|cut -d ' ' -f 1|base64)', '$JWT_AUTH', '$JWT_REFRESH');"
            i=$((i+1))
        done < <(tail -n +2 /config/users.csv)
    fi

    if [ -f "/config/repositories.csv" ]; then
        echo "Creating repositories...."
        i=1
        while IFS="," read -r repo_id repo_uid repo_user_id repo_namespace repo_name repo_slug repo_scm repo_clone_url repo_ssh_url repo_html_url repo_active repo_private repo_visibility repo_branch repo_counter repo_config repo_timeout repo_trusted repo_protected repo_synced repo_created repo_updated repo_version repo_signer repo_secret repo_no_forks repo_no_pulls repo_cancel_pulls repo_cancel_push repo_throttle repo_cancel_running || [ -n "$repo_id" ]; do
            # Validate that repo_name and repo_namespace are not empty
            if [ -z "$repo_name" ] || [ -z "$repo_namespace" ] ||  [ "$repo_namespace/$repo_name" == "repo_namespace/repo_name" ]; then
                echo "Invalid repo: $repo_namespace/$repo_name"
                continue
            fi
            echo "Creating repository: $repo_namespace/$repo_name ($repo_id)"
            if [ "${repo_private,,}" = "true" ]; then
                private=1
            else
                private=0
            fi

            # Create the repository
            sqlite3 /data/database.sqlite "INSERT INTO repos (repo_uid, repo_user_id, repo_namespace, repo_name, repo_slug, repo_clone_url, repo_scm, repo_ssh_url, repo_html_url, repo_active, repo_private, repo_visibility, repo_branch, repo_counter, repo_config, repo_timeout, repo_trusted, repo_protected, repo_synced, repo_created, repo_updated, repo_version, repo_signer, repo_secret, repo_no_forks, repo_no_pulls, repo_cancel_pulls, repo_cancel_push, repo_throttle, repo_cancel_running) VALUES ($repo_uid, $repo_user_id, '$repo_namespace', '$repo_name', '$repo_namespace/$repo_name', '$repo_clone_url', '$repo_scm', '$repo_ssh_url', '$repo_html_url', $repo_active, $private, '$repo_visibility', '$repo_branch', $repo_counter, '$repo_config', $repo_timeout, $repo_trusted, $repo_protected, $repo_synced, $repo_created, $repo_updated, $repo_version, '$repo_signer', '$repo_secret', $repo_no_forks, $repo_no_pulls, $repo_cancel_pulls, $repo_cancel_push, $repo_throttle, $repo_cancel_running);"
            i=$((i+1))
        done < /config/repositories.csv
    fi

    if [ -f "/config/secrets.csv" ]; then
        echo "Creating secrets...."

        while IFS="," read -r repo secret_name secret_data || [ -n "$secret_name" ]; do
            # Validation of Secret Name and Secret Data, 
            if [ -z "$secret_name" ] || [ -z "$secret_data" ] || [ "$secret_name" == "secret_name" ]; then
                echo "Invalid secret: $secret_name"
                continue
            fi
            echo "Creating secret: $secret_name"

            # Create the secret
            sqlite3 /data/database.sqlite "INSERT INTO secrets (secret_repo_id, secret_name, secret_data, secret_pull_request, secret_pull_request_push) VALUES ($repo, '$secret_name', '$secret_data', 1, 1);"

        done < /config/secrets.csv
    fi

    rm /data/NEW_INSTALL
else
    echo "Drone already configured"
fi

echo "Starting Drone..."
exec /bin/drone-server

