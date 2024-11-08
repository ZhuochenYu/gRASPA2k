#!/bin/bash

max_jobs=16  # 最大并行任务数
current_jobs=0

# 遍历所有文件夹
for dir in */; do
    (
        # 检查文件夹名的结尾
        if [[ "$dir" == *1e4/ ]]; then
            # 如果文件夹名以1e4结尾，执行特定命令
            cd "$dir" || exit
            echo -e "101\n\n298,1e4\n\nc2h6,c2h4\n0.5,0.5\n" | gRASPA2k
            cd ..
        elif [[ "$dir" == *1e5/ ]]; then
            # 如果文件夹名以1e5结尾，执行另一命令
            cd "$dir" || exit
            echo -e "101\n\n298,1e5\n\nc2h6,c2h4\n0.5,0.5\n" | gRASPA2k
            cd ..
        fi
    ) &

    current_jobs=$((current_jobs + 1))

    if [ "$current_jobs" -ge "$max_jobs" ]; then
        wait -n  # 等待任意一个后台任务完成
        current_jobs=$((current_jobs - 1))
    fi
done

wait  # 等待所有剩余的后台任务完成

echo "所有任务完成"
