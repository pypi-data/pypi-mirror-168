import os
import click
import subprocess

from teleoss.utils.file_utils import get_dir_files
from teleoss.const.s3cfg import S3CFG
from teleoss.const.click_setting import CONTEXT_SETTINGS


@click.group()
def cli():
    pass


@cli.command('config', short_help='Config teleoss', context_settings=CONTEXT_SETTINGS)
@click.option('--host', prompt='oss address')
@click.option('--access-key', '-ak', prompt='Access Key')
@click.option('--secret-key', '-sk', prompt='Secret Key')
@click.option('--chunk-size', '-cs', type=int, default=1024)
def config(access_key, secret_key, host, chunk_size):
    host = host.split('//')[-1]
    s3cfg_path = os.path.join(os.path.expanduser('~'), '.s3cfg')
    s3cfg_str = S3CFG.format(ak=access_key, sk=secret_key, host=host, cs=chunk_size)
    with open(s3cfg_path, 'w') as file:
        file.write(s3cfg_str)
    click.echo(f'AK: {access_key}\n, SK: {secret_key}\n, host: {host}\n, cs: {chunk_size}')


@cli.command('ls', short_help='List objects or buckets', context_settings=CONTEXT_SETTINGS)
@click.argument('path', default='')
@click.option('--recursive', '-r', is_flag=True, default=False)
def ls(path, recursive):
    if path:
        path = f's3:/{path}' if path.startswith('/') else f's3://{path}'
        if recursive:
            subprocess.call(f's3cmd --recursive ls {path}', shell=True)
        else:
            subprocess.call(f's3cmd ls {path}', shell=True)
    else:
        subprocess.call('s3cmd ls', shell=True)


@cli.command('mb', short_help='Make bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('bucket')
def mb(bucket):
    bucket = f's3://{bucket}'
    subprocess.call(f's3cmd mb {bucket}', shell=True)


@cli.command('rb', short_help='Remove bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('bucket')
@click.option('--force', is_flag=True, default=False)
def rb(bucket, force):
    bucket = f's3://{bucket}'
    if force:
        subprocess.call(f's3cmd rb --force {bucket}', shell=True)
    else:
        subprocess.call(f's3cmd rb {bucket}', shell=True)


@cli.command('la', short_help='List all object in all buckets', context_settings=CONTEXT_SETTINGS)
def la():
    subprocess.call(f's3cmd la', shell=True)


@cli.command('put', short_help='Put file into bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.option('--recursive', '-r', is_flag=True, default=False)
def put(src, dst, recursive):
    src = ' '.join(src)
    dst = f's3:/{dst}' if dst.startswith('/') else f's3://{dst}'
    if recursive:
        subprocess.call(f's3cmd put --recursive {src} {dst}', shell=True)
    else:
        subprocess.call(f's3cmd put {src} {dst}', shell=True)


@cli.command('get', short_help='Get file from bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('path', nargs=-1)
@click.option('--recursive', '-r', is_flag=True, default=False)
def get(path, recursive):
    path = ' '.join(path)
    click.echo(path)
    path = f's3:/{path}' if path.startswith('/') else f's3://{path}'
    if recursive:
        subprocess.call(f's3cmd get --recursive {path}', shell=True)
    else:
        subprocess.call(f's3cmd get {path}', shell=True)


@cli.command('del', short_help='Delete file from bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('path')
@click.option('--recursive', '-r', is_flag=True, default=False)
def delete(path, recursive):
    path = f's3:/{path}' if path.startswith('/') else f's3://{path}'
    if recursive:
        subprocess.call(f's3cmd del --recursive {path}', shell=True)
    else:
        subprocess.call(f's3cmd del {path}', shell=True)


@cli.command('pm', short_help='Put model into bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('project')
@click.argument('path', type=click.Path(exists=True), default='./')
@click.option('--gpu', default='t4')
def pm(project, path, gpu):
    if not os.path.isdir(path):
        click.echo(f'ERROR: {path} is not a folder')
        exit(1)
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            src = os.path.join(dir_path, file_name)
            if file_name == 'config.pbtxt' or file_name == 'labels.txt':
                dir_names = sorted(dir_names, reverse=True)
                dir_name = ''
                for i in range(len(dir_names)):
                    dir_name = dir_names[i]
                    if dir_name.isdigit():
                        break
                if not dir_name:
                    click.echo(f'ERROR: not found version folder in {dir_path}')
                    exit(1)
                dst = os.path.join(dir_path.replace(path, f'/models/{project}/{gpu}/models'), dir_name, file_name)
                dst = f's3:/{dst}'
            else:
                dst = os.path.join(dir_path.replace(path, f'/models/{project}/{gpu}/models'), file_name)
                dst = f's3:/{dst}'
            subprocess.call(f's3cmd put {src} {dst}', shell=True)


@cli.command('gm', short_help='Get model from bucket', context_settings=CONTEXT_SETTINGS)
@click.argument('project')
@click.argument('path', type=click.Path(exists=True))
@click.option('--gpu', default='t4')
def gm(project, path, gpu):
    if not os.path.isdir(path):
        click.echo(f'ERROR: {path} is not a folder')
        exit(1)
    oss_path = f's3://models/{project}/{gpu}/models/'
    status, result = subprocess.getstatusoutput(f's3cmd ls -r {oss_path}')
    srcs = result.split('\n')
    for src in srcs:
        src = src.split(' ')[-1].strip()
        dst = os.path.join(path, src.replace(f's3://models/{project}/{gpu}/', ''))
        subprocess.call(f's3cmd get {src} {dst}', shell=True)
        click.echo(src)
